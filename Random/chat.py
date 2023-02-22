import openai

async def chatgpt(key, prompt):
    openai.api_key = key
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text
    # print(response)
    # with open("test.txt", "wt") as f:
    #     f.write(response.choices[0].text)
