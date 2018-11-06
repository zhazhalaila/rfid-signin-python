import redis, os, base64
import serial, requests
import json
from pusher import Pusher

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

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
secret = os.environ.get('secret') or 'my_spider_key'

while True:
	data = ser.readline()
	if data.startswith(b'Card UID:'):
		data = data.lstrip(b'Card UID:').strip()
		print(data)
		enc = encode(secret, str(data))
		payload = {'rfid_id': enc, 'secret': secret}
		test = requests.get('https://flask-serialshow.herokuapp.com/signin', params=payload)
		print(test.text)
		pusher_client.trigger('message', 'send', {'name': test.text})