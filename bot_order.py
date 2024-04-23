import nextcord
import os
from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = nextcord.Intents.default()
intents.messages = True
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('order-'):
        await message.channel.send(f"Ticket detected: {message.content}")

TOKEN = 'DISCORD_BOT_TOKEN'
client.run(os.getenv('DISCORD_BOT_TOKEN'))
