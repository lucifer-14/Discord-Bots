import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import image_generator as ig
import chat as c
from gtts import gTTS
import asyncio

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
CHATGPT_TOKEN = os.getenv('CHATGPT_TOKEN')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
# bot.channel bot.channels.cache.get("ChannelID")

@bot.event
async def on_ready():
    print("The Bot is Online")

@bot.command()
async def image(ctx, prompt):
    await ig.generate_image(OPENAI_TOKEN, prompt)
    with open('my_image.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)


@bot.command()
async def chat(ctx, *, prompt):
    # Check if the prompt contains the '-tts' flag
    if '-tts' in prompt.lower():
        # Generate a response from the OpenAI GPT model
        response = await c.chatgpt(OPENAI_TOKEN, prompt)
        
        # Send the response as a message to the Discord channel
        await ctx.message.reply(response)
        
        # Remove the flag from the prompt
        prompt = prompt.lower().replace('-tts', '').strip()
        # Convert the response to speech using the gtts library
        response = await c.chatgpt(OPENAI_TOKEN, prompt)
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

    else:
        # Generate a response from the OpenAI GPT model
        response = await c.chatgpt(OPENAI_TOKEN, prompt)
        
        # Send the response as a message to the Discord channel
        await ctx.message.reply(response)


@bot.command()
async def ping(ctx):
    await ctx.send("Were you expecting something?\nIt's me, Pong!")

@bot.command()
async def command_list(ctx):
    await ctx.send("!ping\n!chat \"What is token?\"\n!image \"Some cool image\"")

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


bot.run(BOT_TOKEN)