import requests
import json
import websockets
import time
import asyncio
import aiohttp



class Bot():

	def __init__(self, token):
		self.token = token
		self.loop = asyncio.get_event_loop()
		self.events = {'on_message':[]}
		self.headers = {'authorization': 'Bot ' + token, 'Content-type':'application/json'}


	def add_event(self, event = 'on_message', func = None):

		self.events['on_message'].append(func)


	async def send_json_request(self, ws, request):
		await ws.send(json.dumps(request))

	def start(self):

		asyncio.run(self.run())


	async def receive_json_response(self, ws):

		resp = await ws.recv()
		if resp:
			return json.loads(resp) 


	async def run(self):
		async with websockets.connect('wss://gateway.discord.gg/?v=6&encording=json') as ws:

			payload = {
			"op":2,
			"intents": 513,
			"d": {
				'token': self.token,
				'properties': {
					"$os": 'linux',
					"$browser": 'chrome',
					"$device": 'pc',
				},
				"presence": {
			      "activities": [{
			        "name": "DevIT",
			        "type": 3
			      }],
			      "status": "idle",
			      "since": 91879201,
			      "afk": False
			    },

			},}

			await self.send_json_request(ws, payload)

			while True:
				try:
					event = await self.receive_json_response(ws)
					if event['t'] == 'MESSAGE_CREATE':
						for func in self.events['on_message']:
							message = Message(event['d']['content'], event['d']['author'], event['d']['id'], event['d']['channel_id'], self.token)

							tasks = [asyncio.create_task(func(message))]

						await asyncio.wait(tasks)
						
				except Exception as e:
					print(e)


	async def send_message(self, message = 'Hello, world! I am async discord bot!', channel_id = '1023314181874786314'):
		async with aiohttp.ClientSession(headers = self.headers) as session:
			async with session.post(f'https://discord.com/api/channels/{channel_id}/messages', data = json.dumps({'content':message})) as resp:
				print('Message sent')
				datajson = await resp.json()
				message = Message(datajson['content'], datajson['author'], datajson['id'], datajson['channel_id'], self.token)
				return message




class Message():

	def __init__(self, content, author, id, channel_id, token):
		self.content = content
		self.author = author
		self.id = id
		self.headers = {'authorization': 'Bot ' + token, 'Content-type':'application/json'}
		self.channel_id = channel_id


	async def delete(self):
		async with aiohttp.ClientSession(headers = self.headers) as session:
			async with session.delete(f'https://discord.com/api/channels/{self.channel_id}/messages/{ self.id }') as resp:
				print('Message deletez')
