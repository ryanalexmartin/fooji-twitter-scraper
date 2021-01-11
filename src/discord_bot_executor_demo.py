import time
import asyncio
from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor

def blocking_function():
    print('entering blocking function')
    time.sleep(3)
    print('sleep has been completed')
    return 'Pong'

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('client ready')

@client.command()
async def ping(ctx):
    loop = asyncio.get_event_loop()
    block_return = await loop.run_in_executor(ThreadPoolExecutor(), blocking_function)
    await ctx.send(block_return)

client.run('Nzk2NjAwNjQ3NzA1Mjk2ODk2.X_aSKg.MqfzS-h5YAdZfzHUYgWuQpacQiE')