import discord

from discord import Message, Embed

from env import API_TOKEN
from fiis import build_fiis_msg
from stocks import build_stocks_msg

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message: Message):
        if message.channel.name == 'comandos':
            if '/fiis help' in message.content:
                optionsMsg = '*FIIS Data:* \n';
                optionsMsg += '- Use the command `!fiis` followed by the ticker symbols of the FIIs you\'re interested in. \n'
                optionsMsg += '- You can separate the symbols with spaces, commas, or a mix of both. \n'
                optionsMsg += '*Examples:* \n'
                optionsMsg += '> `!fiis mxrf11 bcff11 xpto11`\n'
                optionsMsg += '> `!fiis xpca11,bcff11,xpto11`\n'
                optionsMsg += '> `!fiis mxrf11, bcff11, xpto11`'

                embed = Embed(title='FIIs help', colour=discord.Colour.purple())
                embed.add_field(name='', value=optionsMsg)
                await message.channel.send(embed=embed)
                return
            elif '/stocks help' in message.content:
                optionsMsg = '*Stocks Data:* \n';
                optionsMsg += '- Use the command `!stocks` followed by the ticker symbols of the Stocks you\'re interested in. \n'
                optionsMsg += '- You can separate the symbols with spaces, commas, or a mix of both.\n'
                optionsMsg += '- You can pass `dividends` to show a table with the dividends history. \n'
                optionsMsg += '*Examples:* \n'
                optionsMsg += '> `!stocks petr4 vale3 itub4`\n'
                optionsMsg += '> `!stocks abev3,petr4,vale3`\n'
                optionsMsg += '> `!stocks itub4, abev3, petr4 dividends`'
                
                embed = Embed(title='Stocks help', colour=discord.Colour.purple())
                embed.add_field(name='', value=optionsMsg)
                await message.channel.send(embed=embed)
                return
            if '/fiis' in message.content:
                await build_fiis_msg(message=message)
            if '/stocks' in message.content:
                await build_stocks_msg(message=message)


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(API_TOKEN)
