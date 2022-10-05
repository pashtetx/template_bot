from app import Bot
import asyncio


token = 'your token'

bot = Bot(token)


# Simle echo bot 


async def on_message(message): # on_message event 

	if message.author['id'] != '1024380985971843092':

		message = await bot.send_message(message.content, channel_id = message.channel_id)
		print(message.content)
		await asyncio.sleep(4)
		await message.delete()



bot.add_event(func = on_message) # add event in bot

bot.start() # connect bot
