FROM python:3.6-alpine

RUN apk add -U --no-cache gcc build-base linux-headers ca-certificates python3 python3-dev libffi-dev libressl-dev

RUN adduser -D serialshow

WORKDIR /home/rfid-signin-python

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn 'pymysql>=0.8.1,<0.9'

COPY app app
COPY migrations migrations
COPY serialshow.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP serialshow.py

RUN chown -R serialshow:root ./
USER serialshow

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
