#!/usr/bin/env python

import os
import sys

import hvac
import jira
import pprint
import requests
import boto3

def get_events():
    
    # Grab account aliases
    iam = boto3.client('iam')
    session = boto3.session.Session()
    ec2 = session.client('ec2',region_name='us-west-1')

    account_aliases = iam.list_account_aliases()['AccountAliases']
    
    regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    events = []
    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        try:
            instances = ec2.describe_instance_status()
        except Exception as e:
            print("Unexpected error: %s" % str(e), file=sys.stderr)
            continue
        print ("Checking %s.." % region)
        
        for i in instances['InstanceStatuses']:
            if i.get('Events'):
                instance_events = [e for e in i.get('Events') if 'Completed' not in e['Description']]
                tags = ec2.describe_tags(Filters=[{
                    'Name': 'resource-id',
                    'Values': [
                        i['InstanceId']
                    ]
                }])
                tags = dict([(t['Key'], t['Value']) for t in tags['Tags']])
                for event in instance_events:
                    e = {
                        'region': region,
                        'instance_id': i['InstanceId'],
                        'instance_name': tags['Name'],
                        'instance_state': i['InstanceState']['Name'],
                        'account_aliases': account_aliases,
                        'event_code': event['Code'],
                        'event_description': event['Description'],
                        'date': event['NotBefore']
                    }
                    events.append(e)
    return events


class JiraCLI:

    def __init__(self,
        jira_url=os.environ['JIRA_URL'],
        jira_user=os.environ['JIRA_USERNAME'],
        jira_pass=os.environ['JIRA_PASSWORD']
    ):
        self.pp = pprint.PrettyPrinter(indent=4)
        self.jira = jira.JIRA(jira_url, basic_auth=(jira_user, jira_pass))
        
    def read(self, fields):
        for issueKey in fields['issues']:
            issue = self.jira.issue(issueKey, expand = True)
            self.pp.pprint(issue.raw)

    def checkFields(self, command, fields):
        for field in self.mustHaveFields[command]:
            if (field not in fields):
                print("Could not find \"{}\" in the file or arguments".format(field))
                return False
        return True

    def create(self, project_key, summary, description, user_name, label, issue_type='Task'):
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': event_description,
            'issuetype': {'name': issue_type},
            'assignee': {'name': user_name},
            'labels': [label],
        }
        if os.environ.get('JIRA_COMPONENT'):
            issue_dict['components'] = [{'name': os.environ.get('JIRA_COMPONENT')}]
        new_issue = self.jira.create_issue(fields=issue_dict)
        print("Issue Key: " + new_issue.key)

    def search(self, jql):
        issue_list = []
        issues = self.jira.search_issues(jql)
        if issues:
            ticket_key=issues[0]
            return ticket_key
        else:
            pass
  
if __name__ == '__main__':
    cli = JiraCLI()
    events = get_events()
    print("\n")
    for event in events:
        print('Instance: %s %s %s' % (event.get('instance_name'), event.get('region'), event.get('account_aliases')))
        print('   Event Type: %s'   % (event.get('event_code')))
        print('   Event Description: %s' % (event.get('event_description')))
        print('   Date: %s' % (event.get('date')))
        jql = " (summary ~ 'Event*' AND summary ~ '%s' ) AND ( status = open OR status = 'IN PROGRESS' ) " % (event['instance_name'])
        if cli.search(jql):
            tvalue = cli.search(jql)
            print("*Not creating a ticket as %s exists*\n" % (tvalue))
        else:
            summary = "AWS Event | %s | %s" % (','.join(event['account_aliases']), event['instance_name'])
            project_key = os.environ.get('JIRA_PROJECT_KEY')
            label = os.environ.get('JIRA_LABEL', 'aws_event')
            user_name = os.environ.get('JIRA_ASSIGNEE', '-1')
            event_description = """
            *AWS Account:*   %s
            *Region:*   %s
            *Instance ID:*   %s
            *Instance Name:*   %s
            *Instance State:*   %s
            *Event:*   %s | %s | %s
            """ % (
                ','.join(event['account_aliases']),
                event['region'],
                event['instance_id'],
                event['instance_name'],
                event['instance_state'],
                event['event_description'],
                event['event_code'],
                event['date'].strftime('%m/%d/%Y %H:%M:%S')
            )
            print("Creating a ticket for %s(%s)" % (event['instance_name'], event['instance_id']))
            cli.create(project_id, project_key, summary, event_description, user_name, label)
            print("\n")