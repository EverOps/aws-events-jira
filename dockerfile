FROM python:3.6.5 
WORKDIR /home/jira

RUN wget https://github.com/Droplr/aws-env/raw/master/bin/aws-env-linux-amd64 -O /bin/aws-env && \
  chmod +x /bin/aws-env

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY get-events.py .
CMD ["/bin/bash", "-c", "eval $(aws-env) && python3 get-events.py"]
