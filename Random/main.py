import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import image_generator as ig
import chat as c

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_TOKEN = os.getenv('OPENAI_TOKEN')
CHATGPT_TOKEN = os.getenv('CHATGPT_TOKEN')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("hello")

@bot.command()
async def image(ctx, prompt):
    await ig.generate_image(OPENAI_TOKEN, prompt)
    with open('my_image.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)


@bot.command()
async def chat(ctx, prompt):
    # await ctx.send(c.chatgpt(OPENAI_TOKEN, prompt))
    with open('test.txt', 'rt') as f:
        await ctx.send(f.read())
    # print(c.chatgpt(OPENAI_TOKEN, prompt))
    # await ctx.send(c.chatgpt(OPENAI_TOKEN, prompt))


bot.run(BOT_TOKEN)