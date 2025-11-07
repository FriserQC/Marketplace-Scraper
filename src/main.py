"""Main Discord bot for Facebook Marketplace scraping."""

import asyncio
import logging
import sys
from datetime import datetime
from typing import List

import discord

from config import config
from listing import Listing
from web_scraper import scrape_marketplace_listings

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Force Discord bot logs to ERROR only (level 40)
logging.getLogger("discord").setLevel(logging.ERROR)
logging.getLogger("discord.client").setLevel(logging.ERROR)
logging.getLogger("discord.gateway").setLevel(logging.ERROR)
logging.getLogger("discord.http").setLevel(logging.ERROR)


class MyClient(discord.Client):
    """Discord client for marketplace scraping bot."""

    def __init__(self, *args, **kwargs):
        self.previous_listings: List[Listing] = []
        self.bg_task = None
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        """Set up background task on client start."""
        self.bg_task = self.loop.create_task(self.background_marketplace_scraping_task())

    async def background_marketplace_scraping_task(self):
        """Background task that scrapes marketplace every 5 minutes."""
        await self.wait_until_ready()
        logger.info("Background scraping task started")

        wanted_channel = self.get_channel(config.FREE_WANTED_CHANNEL_ID)
        misc_channel = self.get_channel(config.FREE_MISC_CHANNEL_ID)
        home_channel = self.get_channel(config.FREE_HOME_CHANNEL_ID)
        unwanted_channel = self.get_channel(config.FREE_UNWANTED_CHANNEL_ID)

        # Verify channels exist
        if not all([wanted_channel, misc_channel, home_channel, unwanted_channel]):
            logger.error("One or more Discord channels not found. Check your channel IDs.")
            return

        while not self.is_closed():
            logger.info("Starting scraping cycle: %s", datetime.now().strftime("%H:%M %B %d, %Y"))

            try:
                listings = await scrape_marketplace_listings(self.previous_listings)
                await self.process_listings(
                    listings,
                    wanted_channel,
                    misc_channel,
                    home_channel,
                    unwanted_channel,
                )

                logger.info(
                    "Scraping cycle completed. Waiting %d minutes for next cycle.",
                    config.SCRAPE_INTERVAL_MINUTES,
                )
                await asyncio.sleep(config.SCRAPE_INTERVAL_MINUTES * 60)

            except Exception as exc:
                logger.exception(
                    "Scraping task error. Retrying in %d minutes... %s",
                    config.SCRAPE_INTERVAL_MINUTES,
                    exc,
                )
                await asyncio.sleep(config.SCRAPE_INTERVAL_MINUTES * 60)

    async def process_listings(
        self,
        listings: List[Listing],
        wanted_channel,
        misc_channel,
        home_channel,
        unwanted_channel,
    ):
        """Process and send listings to appropriate Discord channels."""
        logger.info("Processing %d listings", len(listings))

        new_listings_count = 0
        category_counts = {"wanted": 0, "home": 0, "misc": 0, "unwanted": 0}

        for listing in listings:
            if not listing.is_previous:
                new_listings_count += 1

                message = (
                    f"Location: {listing.location.strip()}\n"
                    f"General Category: {listing.general_category}\n"
                    f"Specific Category: {listing.specific_category}\n"
                    f"Title: {listing.title}\n"
                    f"Image: {listing.img_url}\n"
                    f"URL: {listing.url}\n"
                )

                try:
                    if listing.is_unwanted:
                        await unwanted_channel.send(message)
                        category_counts["unwanted"] += 1
                    elif listing.is_wanted:
                        await wanted_channel.send(message)
                        category_counts["wanted"] += 1
                    elif listing.is_home:
                        await home_channel.send(message)
                        category_counts["home"] += 1
                    else:
                        await misc_channel.send(message)
                        category_counts["misc"] += 1

                    self.previous_listings.append(listing.url)

                except discord.HTTPException as exc:
                    logger.error("Failed to send message to Discord: %s", exc)
                except Exception as exc:
                    logger.exception("Unexpected error sending listing: %s", exc)

        # Log summary
        logger.info(
            "Sent %d new listings - Wanted: %d, Home: %d, Misc: %d, Unwanted: %d",
            new_listings_count,
            category_counts["wanted"],
            category_counts["home"],
            category_counts["misc"],
            category_counts["unwanted"],
        )

        # Clear previous data
        logger.info("Total previous listings tracked: %d", len(self.previous_listings))
        while len(self.previous_listings) > config.MAX_PREVIOUS_LISTINGS:
            self.previous_listings.pop(0)

        logger.info("Cycle ended: %s\n", datetime.now().strftime("%H:%M %B %d, %Y"))


client = MyClient(intents=discord.Intents.default())


async def main():
    """Main entry point for the Discord bot."""
    try:
        logger.info("Starting Discord bot...")
        await client.start(config.DISCORD_TOKEN, reconnect=True)
    except discord.LoginFailure:
        logger.error("Invalid Discord token. Check your DISCORD_TOKEN in .env file.")
    except discord.HTTPException as exc:
        if exc.status == 429:
            retry_after = exc.response.headers.get("Retry-After")
            logger.error("Rate limit hit! Retry after: %s seconds.", retry_after)
        else:
            logger.error("HTTPException occurred: %s", exc)
    except Exception as exc:
        logger.exception("An unexpected error occurred: %s", exc)
    finally:
        if not client.is_closed():
            await client.close()
            logger.info("Bot stopped gracefully")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt)")
    except Exception as exc:
        logger.exception("Fatal error: %s", exc)
        sys.exit(1)
