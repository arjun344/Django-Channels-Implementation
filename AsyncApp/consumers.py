import asyncio
import json
from channels.consumer import AsyncConsumer

class ChatConsumer(AsyncConsumer):
	async def websocket_connect(self,event):
		print("connected",event)
		with open('Database/database.json', 'r') as openfile:
					json_object = json.load(openfile)

		await self.send({
			"type":"websocket.accept"
			})

		await self.send({
			"type":"websocket.send",
			"text": str(json_object).replace("'",'"')
			})

		self.broadcast_room = f"evreyone"

		await self.channel_layer.group_add(
			self.broadcast_room,
			self.channel_name
			)


	async def websocket_receive(self,event):
		data = event.get('text',None)
		print(data)
		if data is not None:
			data = json.loads(data)
			message = data.get('text')
			req_type = data.get('type')
			print(req_type)
			if req_type == 'websocket_receive_ques':
				ques = message.get('message')
				with open('Database/database.json', 'r') as openfile:
					json_object = json.load(openfile)
					ques_id = len(json_object) + 1
					insert_data = {"ques":ques,"ans":"None"}
					json_object[str(ques_id)] = insert_data

				with open("Database/database.json", "w") as outfile: 
					json.dump(json_object, outfile, indent = 4)

					await self.send({
						"type":"websocket.send",
						"text": str(json_object).replace("'",'"')
					})

					await self.channel_layer.group_send(
						self.broadcast_room,
							{
								"type":"broadcast_message",
								"text": str(json_object).replace("'",'"')
							}
						)

			elif req_type == 'websocket_receive_ans':

				ques_id = message.get("id")
				ans = message.get("message")
				with open('Database/database.json', 'r') as openfile:
					json_object = json.load(openfile)
					json_object[str(ques_id)]['ans'] = ans

				with open("Database/database.json", "w") as outfile: 
					json.dump(json_object, outfile, indent = 4)

					await self.send({
						"type":"websocket.send",
						"text": str(json_object).replace("'",'"')
					})

					await self.channel_layer.group_send(
						self.broadcast_room,
							{
								"type":"broadcast_message",
								"text": str(json_object).replace("'",'"')
							}
						)






	async def broadcast_message(self,event):
		print("message",event)

		await self.send({
						"type":"websocket.send",
						"text": event['text']
					})


	async def websocket_disconnect(self,event):
		print("disconnected",event)