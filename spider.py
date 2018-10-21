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

r = redis.StrictRedis(host='localhost', port=6379, db=0)
token = r.get('curr_token')

while True:
	data = ser.readline()
	if data.startswith(b'Card UID:'):
		data = data.lstrip(b'Card UID:').strip()
		payload = {'token': token, 'rfid_id': data}
		test = requests.get('http://127.0.0.1:5000/signin', params=payload)
		pusher_client.trigger('message', 'send', {'name': test.text})