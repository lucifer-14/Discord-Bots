import discord
from discord.ext import commands
import os
import youtube_dl

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)




bot = commands.Bot(command_prefix='-', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("hello")
    # channel = bot.get_channel(CHANNEL_ID)
    # print(channel)
    # await channel.send("Hello abc")

@bot.command()
async def hello(ctx):
    await ctx.send("hello world")


@bot.command()
async def s(ctx, name):
    # print(repr(ctx))
    await ctx.send(f's paw {name}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def command_list(ctx):
    await ctx.send('ping\ns_paw')

@bot.command()
async def play(ctx):
    # await
    pass

bot.run(TOKEN)