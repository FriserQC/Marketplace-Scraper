import discord
from discord.ext import tasks
from WebScraper import GetMessage
import asyncio

import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = (int)(os.getenv("CHANNEL_ID"))
MAX_NUMBER_OF_PREVIOUS_LISTINGS = 300

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
            messages = await GetMessage(self.previousListings)
            for infos in messages:
                url = infos[2]
                if url not in self.previousListings:
                    message = (f'Title: {infos[0].strip()}\nLocation: {infos[1].strip()}\nURL: {url}\n\n')
                    await channel.send(message)
                    self.previousListings.append(url)

            print("number of previous listings : " + str(len(self.previousListings)))

            # clear previous data 
            if len(self.previousListings) > MAX_NUMBER_OF_PREVIOUS_LISTINGS:
                while (len(self.previousListings) > MAX_NUMBER_OF_PREVIOUS_LISTINGS):
                    self.previousListings.pop(0)

            await asyncio.sleep(600)  # task runs every 10 minutes


client = MyClient(intents=discord.Intents.default())
client.run(TOKEN)
#client.run(TOKEN, log_handler=None)