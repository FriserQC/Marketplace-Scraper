import discord
from discord.ext import tasks
from Scrapper import GetMessage
import datetime
import asyncio

import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = (int)(os.getenv("CHANNEL_ID"))

class MyClient(discord.Client):
    previousListings = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def my_background_task(self):
        await self.wait_until_ready()
        channel = client.get_channel(CHANNEL_ID)  # channel ID goes here
        while not self.is_closed():
            # sends every message
            messages = await GetMessage()
            for message in messages:
                if message not in self.previousListings:
                    await channel.send(message)
                    self.previousListings.append(message)

            # clear previous data 
            if len(self.previousListings) > 80:
                while (len(self.previousListings) > 80):
                    self.previousListings.pop(0)

            await asyncio.sleep(60)  # task runs every 1 minutes


client = MyClient(intents=discord.Intents.default())
client.run(TOKEN)
#client.run(TOKEN, log_handler=None)