FROM python:3.9-slim

ARG APP_HOME=/usr/src
RUN apt-get update && apt-get install -y build-essential gcc

WORKDIR ${APP_HOME}
COPY . ${APP_HOME}
# RUN pip install --upgrade pip && pip install pipenv && pipenv requirements > requirements.txt
RUN pip install --no-cache-dir -r ${APP_HOME}/requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD ["python", "app.py"]
