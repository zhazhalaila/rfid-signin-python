import serial, requests
import json
from bs4 import BeautifulSoup
import requests
from pusher import Pusher

ser = serial.Serial('COM3', 9600)
pusher_client = Pusher(
  app_id='621177',
  key='b5b7012005f41774f901',
  secret='b996e0df93996214b5ae',
  cluster='ap1',
  ssl=True
)

r = requests.get('https://flask-serialshow.herokuapp.com/online')
soup = BeautifulSoup(r.text, 'html.parser')
token = soup.find("div", {"data-title": "Token"}).string.strip()
print(token)
while True:
	data = ser.readline()
	if data.startswith(b'Card UID:'):
		data = data.lstrip(b'Card UID:').strip()
		payload = {'token': token, 'rfid_id': data}
		test = requests.get('https://flask-serialshow.herokuapp.com/signin', params=payload)
		print(test.text)
		pusher_client.trigger('message', 'send', {'name': test.text})