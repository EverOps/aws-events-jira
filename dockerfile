FROM python:3.6.5 
WORKDIR /home/jira
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY get-events.py .
<<<<<<< Updated upstream
COPY start.sh start.sh
CMD [ "python3", "get-events.py"]
=======
CMD ["/bin/bash", "-c", "python3 get-events.py"]
>>>>>>> Stashed changes
