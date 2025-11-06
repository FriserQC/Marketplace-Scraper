import os
from datetime import datetime
import asyncio
import async_timeout
from dotenv import load_dotenv
import discord
from web_scraper import scrape_marketplace_listings
from typing import List

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
FREE_WANTED_CHANNEL_ID = int(os.getenv("FREE_WANTED_CHANNEL_ID"))
FREE_MISC_CHANNEL_ID = int(os.getenv("FREE_MISC_CHANNEL_ID"))
FREE_HOME_CHANNEL_ID = int(os.getenv("FREE_HOME_CHANNEL_ID"))
FREE_UNWANTED_CHANNEL_ID = int(os.getenv("FREE_UNWANTED_CHANNEL_ID"))
MAX_NUMBER_OF_PREVIOUS_LISTINGS = 1000

class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        self.previous_listings: List[str] = []
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.background_marketplace_scraping_task())

    async def background_marketplace_scraping_task(self):
        await self.wait_until_ready()

        wanted_channel = self.get_channel(FREE_WANTED_CHANNEL_ID)
        misc_channel = self.get_channel(FREE_MISC_CHANNEL_ID)
        home_channel = self.get_channel(FREE_HOME_CHANNEL_ID)
        unwanted_channel = self.get_channel(FREE_UNWANTED_CHANNEL_ID)

        while not self.is_closed():
            print("Start: " + datetime.now().strftime("%H:%M %B %d, %Y"))

            try:
                listings = await scrape_marketplace_listings(self.previous_listings)
                await self.process_listings(listings, wanted_channel, misc_channel, home_channel, unwanted_channel)             

                await asyncio.sleep(5 * 60)  # Task runs every 5 minutes

            except Exception as e:
                print(f"Scraping task error. Retrying... {e}")

    async def process_listings(self, listings: List, wanted_channel, misc_channel, home_channel, unwanted_channel):
        print(f'Sending listings in discord')
        for listing in listings:
            if not listing.is_previous:
                message = (f'Location: {listing.location.strip()}\n'
                           f'General Category: {listing.general_category}\n'
                           f'Specific Category: {listing.specific_category}\n'
                           f'Title: {listing.title}\n'
                           f'Image: {listing.img_url}\n'
                           f'URL: {listing.url}\n')

                if listing.is_unwanted:
                    await unwanted_channel.send(message)
                elif listing.is_wanted:
                    await wanted_channel.send(message)
                elif listing.is_home:
                    await home_channel.send(message)
                else:
                    await misc_channel.send(message)
                    
                self.previous_listings.append(listing.url)

        # Clear previous data
        print(f'Number of previous listings: {len(self.previous_listings)}')
        while len(self.previous_listings) > MAX_NUMBER_OF_PREVIOUS_LISTINGS:
            self.previous_listings.pop(0)

        print("End: " + datetime.now().strftime("%H:%M %B %d, %Y") + "\n")

client = MyClient(intents=discord.Intents.default())

async def main():
    try:
        await client.start(TOKEN, reconnect=True)
    except discord.HTTPException as e:
        # Check for rate limit (HTTP 429)
        if e.status == 429:
            retry_after = e.response.headers.get("Retry-After")
            message = f"Rate limit hit! Retry after: {retry_after} seconds."
            print(message)
        else:
            print(f"HTTPException occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while running the bot: {e}")
    finally:
        # Properly close the connection
        if not client.is_closed():
            await client.close()
        
        # Give time for cleanup
        await asyncio.sleep(1)
        
        # Restart (use correct path for container)
        os.system("python src/restarter.py")
        os.system('kill 1')

if __name__ == "__main__":
    asyncio.run(main())
