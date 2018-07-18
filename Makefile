build:
	docker build -t everops/aws-jira-events .

run: build
	docker run \
	-e AWS_PROFILE \
	-e AWS_ACCESS_KEY_ID \
	-e AWS_SECRET_ACCESS_KEY \
	-e JIRA_URL \
	-e JIRA_USERNAME \
	-e JIRA_PASSWORD \
	-v ~/.aws/:/root/.aws \
	-ti everops/aws-jira-events
