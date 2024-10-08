import discord
from discord.ext import tasks 
from web_scraper import extract_wanted_listings
import asyncio
import datetime

import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 

TOKEN = os.getenv("DISCORD_TOKEN")
FREE_MISC_CHANNEL_ID = (int)(os.getenv("FREE_MISC_CHANNEL_ID"))
FREE_FURNITURE_CHANNEL_ID = (int)(os.getenv("FREE_FURNITURE_CHANNEL_ID"))
FREE_UNWANTED_CHANNEL_ID = (int)(os.getenv("FREE_UNWANTED_CHANNEL_ID"))
MAX_NUMBER_OF_PREVIOUS_LISTINGS = 500

class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        self.previousListings = []
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def my_background_task(self):
        await self.wait_until_ready()

        miscChannel = client.get_channel(FREE_MISC_CHANNEL_ID)
        furnitureChannel = client.get_channel(FREE_FURNITURE_CHANNEL_ID)
        unwantedChannel = client.get_channel(FREE_UNWANTED_CHANNEL_ID)
        
        while not self.is_closed():
            print("Start : " + datetime.datetime.now().strftime("%H:%M %B %d, %Y"))

            # sends every message
            listings = await extract_wanted_listings(self.previousListings)
            for listing in listings:
                if listing.isPrevious == False:
                    message = (f'Title: {listing.title.strip()}\nLocation: {listing.location.strip()}\nURL: {listing.url}\n\n')

                    if listing.isUnwanted == True:
                        await unwantedChannel.send(message)
                    elif listing.isFurniture == True:
                        await furnitureChannel.send(message)
                    else :
                        await miscChannel.send(message)
                    self.previousListings.append(listing.url)

            print("number of previous listings : " + str(len(self.previousListings)))

            # clear previous data 
            if len(self.previousListings) > MAX_NUMBER_OF_PREVIOUS_LISTINGS:
                while (len(self.previousListings) > MAX_NUMBER_OF_PREVIOUS_LISTINGS):
                    self.previousListings.pop(0)

            print("End : " + datetime.datetime.now().strftime("%H:%M %B %d, %Y"))
            print('------')

            await asyncio.sleep(300)  # task runs every 5 minutes


client = MyClient(intents=discord.Intents.default())
client.run(TOKEN, reconnect=True, log_level=50)