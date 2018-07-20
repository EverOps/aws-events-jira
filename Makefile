build:
	docker build -t everops/aws-events-jira .

run: build
	docker run \
	-e AWS_PROFILE \
	-e AWS_ACCESS_KEY_ID \
	-e AWS_SECRET_ACCESS_KEY \
	-e AWS_REGION \
	-e JIRA_URL \
	-e AWS_ENV_PATH \
	-v ~/.aws/:/root/.aws \
	-ti everops/aws-events-jira

push: build
	docker push everops/aws-events-jira
