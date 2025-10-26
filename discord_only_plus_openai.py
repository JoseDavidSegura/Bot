from dotenv import load_dotenv
from openai import OpenAI
import discord
import os

#set openai api key
load_dotenv()
openai_api_key = os.getenv('OPENAI_KEY')
oa_client = OpenAI(api_key=openai_api_key)

# ask openai response like a thanos
def call_openai(question):
    #call openai api
    completion = oa_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": f"Respond like a thanos from marvel movies to the following question: {question}",
            },
        ]
    )

    #print the response 
    response = completion.choices[0].message.content
    print(response)
    return response

#setup intents
intents = discord.Intents.default()
intents.message_content = True  # Ensure that your bot can read message content
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hola'):
        await message.channel.send('Hola!')

    if message.content.startswith('$question'):
        print(f"Message: {message.content}")
        message_content = message.content.split("$question")[1]
        print(f"Question: {message_content}")
        response = call_openai(message_content)
        print(f"Assistant: {response}")
        print("---")
        await message.channel.send(response)

client.run(os.getenv('TOKEN'))
