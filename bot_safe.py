
import os
import asyncio
import threading
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("MTM4MjQ2Mjk1MTAwNDMwNzUwNg.GQfe9N.V6_IUuGSEVsUm1Jdo3-lKxboJQhnvzbsnMH6vE")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)
app = Flask(__name__)
loop = asyncio.new_event_loop()

@app.route('/')
def index():
    return "🟢 Flask сервер работает!"

@app.route('/send', methods=['POST'])
def send_dm():
    data = request.get_json()
    user_id = data.get("user_id")
    message = data.get("message")

    if not user_id or not message:
        return jsonify({'error': 'user_id and message required'}), 400

    async def dm():
        try:
            user = await bot.fetch_user(int(user_id))
            if user:
                await user.send(message)
        except Exception as e:
            print(f"❌ Ошибка отправки: {e}")

    asyncio.run_coroutine_threadsafe(dm(), loop)
    return jsonify({'status': 'ok'}), 200

@bot.event
async def on_ready():
    print(f"✅ Бот запущен как {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"🔊 Зашёл в канал: {channel.name}")
    else:
        await ctx.send("❌ Ты не в голосовом канале!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Вышел из голосового канала.")
    else:
        await ctx.send("❌ Я не в голосовом канале.")

def run_bot():
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.start(MTM4MjQ2Mjk1MTAwNDMwNzUwNg.GQfe9N.V6_IUuGSEVsUm1Jdo3-lKxboJQhnvzbsnMH6vE))

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=5000)
