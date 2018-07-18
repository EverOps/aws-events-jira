# aws-events-jira
Generates and runs a docker container that executes python script to query nodes with scheduled events in AWS and creates a ticket in Jira for each node (if a ticket doesn't exist)

# Usage
While this image can be run locally, it is meant to be run on a scheduled interval via some other process. 

To run it locally, use the `Makefile`
```
make run
```
The `Makefile` will forward several environment variables `AWS_ACCESS_KEY_ID` and `JIRA_URL` into the container. 
These evironment variables are required to be set for this script.

```
AWS_ACCESS_KEY_ID - AWS Authentication, not needed if credentials are set via instance role or other.
AWS_SECRET_ACCESS_KEY - AWS Authentication, not needed if credentials are set via instance role or other.
JIRA_URL - The URL to JIRA. i.e https://everops.atlassian.net
JIRA_USERNAME - The username to use when authenticating with JIRA
JIRA_PASSWORD - The password to use when authenticating with JIRA
```

### Usage
`make run`
