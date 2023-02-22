from PIL import Image
import requests
import shutil
import openai
import discord

async def generate_image(key: str, prompt: str):
    openai.api_key = key
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']

    with open('my_image.png', 'wb') as file:
        shutil.copyfileobj(requests.get(image_url, stream=True).raw, file)