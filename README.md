# aws-events-jira
Generates and runs a docker container that executes python script to query nodes with scheduled events in AWS and creates a ticket in Jira for each node (if a ticket doesn't exist)

# Usage
While this image can be run locally, it is meant to be run on a scheduled interval via some other process. 

To run it locally, use the `Makefile`
```
make run
```
The `Makefile` will forward several environment variables `AWS_ACCESS_KEY_ID` and `GITHUB_ACCESS_TOKEN` into the container. 
These evironment ariables are required to be set for this script.

```
AWS_ACCESS_KEY_ID - AWS Authentication, not needed if credentials are set via instance role or other.
AWS_SECRET_ACCESS_KEY - AWS Authentication, not needed if credentials are set via instance role or other.
GITHUB_ACCESS_TOKEN - A personal access token, used to authenticate to vault server.
VAULT_PATH - Path where JIRA credentials are stored within vault
JIRA_URL - The URL to JIRA. i.e https://everops.atlassian.net
```

### Usage
`make run`
