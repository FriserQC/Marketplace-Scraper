import discord
from discord.ext import tasks
from Scrapper import GetMessage
import datetime

import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNELID = os.getenv("CHANNEL_ID")
5
class MyClient(discord.Client):
    previousListings = []
    counter = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=600)  # task runs every 600 seconds
    async def my_background_task(self):
        print("Started loop at " + datetime.datetime.now().strftime("%H:%M %B %d, %Y"))

        channel = self.get_channel(CHANNELID)  # channel ID goes here
        messages = await GetMessage()
        for message in messages:
            if message not in self.previousListings:
                await channel.send(message)
                self.previousListings.append(message)

        self.counter +=1

        # clear previous data 
        if self.counter > 20:
            self.counter = 0
            while (len(self.previousListings) > 80):
                self.previousListings.pop(0)

        print("Finished loop at " + datetime.datetime.now().strftime("%H:%M %B %d, %Y"))

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


client = MyClient(intents=discord.Intents.default())
client.run(TOKEN, log_handler=None)