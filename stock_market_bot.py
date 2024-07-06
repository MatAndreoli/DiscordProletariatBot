import discord

from discord import Message

from env import API_TOKEN
from fiis import build_fiis_msg
from stocks import build_stocks_msg

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message: Message):
        if message.channel.name == 'comandos':
            if '/fiis' in message.content:
                await build_fiis_msg(message=message)
            if '/stocks' in message.content:
                await build_stocks_msg(message=message)


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(API_TOKEN)
