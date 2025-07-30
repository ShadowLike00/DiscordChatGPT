# This example requires the 'message_content' intent.
#Application Id:1399951252045168670
#Public Key:a880ff873bf7d71be341cbbce3f020fd5f084c45f2b8513f23ca3c7f03191f44

from typing import AnyStr
import discord
import os
import requests
from dotenv import load_dotenv
from keep_alive import keep_alive

with open("chat.txt", "r") as f:
    chat=f.read()
    
# Load .env or Replit Secrets
load_dotenv()
DISCORD_TOKEN = os.getenv("SECRET_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Setup Discord bot intents
intents = discord.Intents.default()
intents.message_content = True

# Function to call Groq API
def ask_groq(message_content):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct", 
        "messages": [
            {"role": "system", "content": "You are ZenX, a helpful AI assistant."},
            {"role": "user", "content": f"{chat}\nZenXGPT: "}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Groq Error {response.status_code}: {response.text}"

# Discord bot class
class MyClient(discord.Client):
    async def on_ready(self):
        print(f"✅ Bot is live as {self.user}")

    async def on_message(self, message):
        global chat
        chat += f"{message.author}: {message.content}\n"
        if message.author == self.user:
            return

        if self.user in message.mentions:
            print(chat)
            print(f"📝 Message from {message.author}: {message.content}")
            await message.channel.send("💭 Thinking...")
            try:
                reply = ask_groq(message.content)
                await message.channel.send(reply)
            except Exception as e:
                # Split into chunks of max 2000 characters
                if len(reply) <= 2000:
                    await message.channel.send(reply)
                else:
                    for i in range(0, len(reply), 2000):
                        await message.channel.send(reply[i:i+2000])


client = MyClient(intents=intents)
keep_alive()
client.run(DISCORD_TOKEN)
