Purpose
------
Generates and runs a docker container that executes python script to query nodes with scheduled events in AWS and creates a ticket in Jira for each node (if a ticket doesn't exist)

### Requirements
* Docker
* Following ENV Variables set with appropriate values
  * AWS_ACCESS_KEY_ID
  * AWS_SECRET_ACCESS_KEY
  * GITHUB_ACCESS_TOKEN
  * VAULT_PATH
  * JIRA_URL

### Usage
`make run`
