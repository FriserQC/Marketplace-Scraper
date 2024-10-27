import os
import datetime
import asyncio
from dotenv import load_dotenv
import discord
from web_scraper import scrape_wanted_listings

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
FREE_MISC_CHANNEL_ID = int(os.getenv("FREE_MISC_CHANNEL_ID"))
FREE_FURNITURE_CHANNEL_ID = int(os.getenv("FREE_FURNITURE_CHANNEL_ID"))
FREE_UNWANTED_CHANNEL_ID = int(os.getenv("FREE_UNWANTED_CHANNEL_ID"))
MAX_NUMBER_OF_PREVIOUS_LISTINGS = 500

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        self.previous_listings = []
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        # Create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.background_marketplace_scraping_task())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def background_marketplace_scraping_task(self):
        await self.wait_until_ready()

        misc_channel = self.get_channel(FREE_MISC_CHANNEL_ID)
        furniture_channel = self.get_channel(FREE_FURNITURE_CHANNEL_ID)
        unwanted_channel = self.get_channel(FREE_UNWANTED_CHANNEL_ID)

        while not self.is_closed():
            print("Start: " + datetime.datetime.now().strftime("%H:%M %B %d, %Y"))

            # Run task; if it takes more than 15 minutes, cancel and retry
            try:
                async with asyncio.timeout(900):
                    listings = await scrape_wanted_listings(self.previous_listings)
                    for listing in listings:
                        if not listing.is_previous:
                            message = (f'Location: {listing.location.strip()}\n'
                                       f'General Category: {listing.general_category}\n'
                                       f'Specific Category: {listing.specific_category}\n'
                                       f'URL: {listing.url}\n')

                            if listing.is_unwanted:
                                await unwanted_channel.send(message)
                            elif listing.is_furniture:
                                await furniture_channel.send(message)
                            else:
                                await misc_channel.send(message)
                            self.previous_listings.append(listing.url)

                    print(f'Number of previous listings: {len(self.previous_listings)}')

                    # Clear previous data
                    while len(self.previous_listings) > MAX_NUMBER_OF_PREVIOUS_LISTINGS:
                        self.previous_listings.pop(0)

                    print("End: " + datetime.datetime.now().strftime("%H:%M %B %d, %Y"))
                    print('------')

                await asyncio.sleep(300)  # Task runs every 5 minutes

            except Exception as e:
                print(f'The scraper operation took too long, going to retry: {e}')

client = MyClient(intents=discord.Intents.default())
client.run(TOKEN, reconnect=True, log_level=40)
