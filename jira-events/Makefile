build:
	docker build -t davis/jira-events .

run: build
	docker run \
	-e AWS_ACCESS_KEY_ID \
	-e AWS_SECRET_ACCESS_KEY \
	-e GITHUB_ACCESS_TOKEN \
	-e VAULT_PATH \
	-e JIRA_URL \
	-ti davis/jira-events
