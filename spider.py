import redis
import serial, requests
import json
from pusher import Pusher

ser = serial.Serial('COM3', 9600)
pusher_client = Pusher(
  app_id='621177',
  key='b5b7012005f41774f901',
  secret='b996e0df93996214b5ae',
  cluster='ap1',
  ssl=True
)

pool = redis.ConnectionPool(host='redis://rediscloud:HhtJfAXEbZlWJL8X43qW3ofDxmItRcjX@redis-16318.c9.us-east-1-4.ec2.cloud.redislabs.com:16318', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
token = r.get('curr_token')

while True:
	data = ser.readline()
	if data.startswith(b'Card UID:'):
		data = data.lstrip(b'Card UID:').strip()
		payload = {'token': token, 'rfid_id': data}
		test = requests.get('https://flask-serialshow.herokuapp.com/signin', params=payload)
		print(test.text)
		pusher_client.trigger('message', 'send', {'name': test.text})