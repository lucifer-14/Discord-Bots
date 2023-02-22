import openai

async def chatgpt(key, prompt):
    openai.api_key = key
    response = openai.Completion.create(
            engine='davinci',
            prompt=prompt,
            max_tokens=60,
            n=1,
            stop=None,
            temperature=0.5,
        )
    return response.choices[0].text
