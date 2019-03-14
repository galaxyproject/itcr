# debian:stretch
FROM python:3.7-stretch

SHELL ["/bin/bash", "-c"]

WORKDIR /home/app
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY . .
COPY boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

EXPOSE 5000
ENTRYPOINT ["/bin/bash", "-c" ,"./boot.sh"]
