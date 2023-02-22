import discord
import openai
import os
from dotenv import load_dotenv

load_dotenv()


client = discord.Client()
openai.api_key = os.getenv('API_SECRET')

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('-p'):
        prompt = message.content[3:] # Extract the text after "-p "

        response = openai.Completion.create(
            engine='davinci',
            prompt=prompt,
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.5,
        )

        await message.channel.send(response.choices[0].text)

client.run('your_bot_token_here')

