FROM python:3.6-alpine

RUN adduser -D serialshow

WORKDIR /home/rfid-signin-python

RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY serialshow.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP serialshow.py

RUN chown -R seiralshow:serialshow ./
USER serialshow

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
