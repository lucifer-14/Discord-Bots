import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import image_generator as ig
import chat as c
import youtube_dl
import asyncio
from gtts import gTTS

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
CHATGPT_TOKEN = os.getenv('CHATGPT_TOKEN')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
# bot.channel bot.channels.cache.get("ChannelID")


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



@bot.event
async def on_ready():
    print("The Bot is Online")

@bot.command()
async def image(ctx, prompt):
    async with ctx.typing():
        await ig.generate_image(OPENAI_TOKEN, prompt)
        with open('my_image.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)


@bot.command()
async def chat(ctx, prompt):
    async with ctx.typing():
        await ctx.send(await c.chatgpt(OPENAI_TOKEN, prompt))

@bot.command()
async def chat_tts(ctx, prompt):
    async with ctx.typing():
        await ctx.send(await c.chatgpt(OPENAI_TOKEN, prompt), tts=True)

@bot.command()
async def chat_tts2(ctx, *, prompt):
    # Send a "thinking" message to the channel
    async with ctx.typing():
    # Generate a response from the OpenAI GPT model
        response = await c.chatgpt(OPENAI_TOKEN, prompt)
    # Send the response as a message to the Discord channel
    await ctx.message.reply(response)
    # Check if the prompt contains the '-tts' flag
    if '-tts' in prompt.lower():
        # Remove the flag from the prompt
        prompt = prompt.lower().replace('-tts', '').strip()
        # Convert the response to speech using the gtts library
        tts = gTTS(response)
        tts.save('speech.mp3')

        # Connect to the voice channel of the user who sent the command
        voice = await ctx.author.voice.channel.connect()

        # Play the speech to the voice channel
        audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable="C:/FFmpeg/bin/ffmpeg.exe", source="speech.mp3"))
        voice.play(audio_source)

        # Wait until the speech is finished playing and then disconnect from the voice channel
        while voice.is_playing():
            await asyncio.sleep(1)
        await voice.disconnect()


@bot.command()
async def ping(ctx):
    async with ctx.typing():
        await ctx.send("Were you expecting something?\nIt's me, Pong!")

@bot.command()
async def command_list(ctx):
    async with ctx.typing():
        await ctx.send("!ping\n!chat \"What is token?\"\n!image \"Some cool image\"\n!chat_tts \"What is token?\"")

# @bot.command()
# async def slash_test(ctx):
#     await ctx.send("`lol`")

@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    # print(channel)
    # if ctx.voice_client is not None:
    #     return await ctx.voice_client.move_to(channel)
    
    await channel.connect()
    await ctx.guild.change_voice_state(channel=channel, self_deaf=True)

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command()
async def play(ctx, query):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
    ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

# @bot.command()
# async def test(ctx):
#     await ctx.send("/tts hello", tts=True)

bot.run(BOT_TOKEN)