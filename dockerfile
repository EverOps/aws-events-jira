FROM python:3.6.5 
WORKDIR /home/jira
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY get-events.py .
CMD ["/bin/bash", "-c", "eval $(aws-env) && python3 get-events.py"]
