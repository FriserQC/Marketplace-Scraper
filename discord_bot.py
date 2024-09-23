import discord
from discord.ext import tasks
from web_scraper import extract_listings
import asyncio
import datetime

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
            print("Start : " + datetime.datetime.now().strftime("%H:%M %B %d, %Y"))
            # sends every message
            listings = await extract_listings(self.previousListings)
            for listing in listings:
                url = listing[2]
                if url not in self.previousListings:
                    message = (f'Title: {listing[0].strip()}\nLocation: {listing[1].strip()}\nURL: {url}\n\n')
                    await channel.send(message)
                    self.previousListings.append(url)

            print("number of previous listings : " + str(len(self.previousListings)))

            # clear previous data 
            if len(self.previousListings) > MAX_NUMBER_OF_PREVIOUS_LISTINGS:
                while (len(self.previousListings) > MAX_NUMBER_OF_PREVIOUS_LISTINGS):
                    self.previousListings.pop(0)

            print("End : " + datetime.datetime.now().strftime("%H:%M %B %d, %Y"))

            await asyncio.sleep(600)  # task runs every 10 minutes


client = MyClient(intents=discord.Intents.default())
client.run(TOKEN)
#client.run(TOKEN, log_handler=None)