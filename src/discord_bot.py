# This bot handles Discord logins and config issues, and runs in the background while the scraper runs in a loop.

from modules.cogs.scrape_cog import ScrapeCog
from modules.config import auth_token, channel_id
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", case_insensitive=True)
bot.add_cog(ScrapeCog(bot))


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

bot.run(auth_token)