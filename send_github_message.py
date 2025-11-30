import asyncio
from pyrogram import Client, filters
import aiohttp

# Telegram API bilgilerin
api_id = 20053879
api_hash = "78356e55bacd8c7fa1b188b4c9c88929"
session_name = "Apozazaxva"  # .session dosyası oluşturulacak

# GitHub raw linkindeki mesaj.txt
GITHUB_RAW_URL = "https://raw.githubusercontent.com/02Apo02/Mesaj-bot/main/Mesaj.txt"

# Mesaj göndereceğin grupların ID'leri
GROUP_IDS = []

app = Client(session_name, api_id=api_id, api_hash=api_hash)

# GitHub'dan mesajı oku
async def get_github_message():
    async with aiohttp.ClientSession() as session:
        async with session.get(GITHUB_RAW_URL) as resp:
            return await resp.text()

# Gruplara mesaj gönder
async def send_messages():
    await app.start()
    while True:
        mesaj = await get_github_message()
        for gid in GROUP_IDS:
            try:
                await app.send_message(gid, mesaj)
                print(f"{gid} grubuna mesaj gönderildi.")
            except Exception as e:
                print(f"Hata {gid}: {e}")
        await asyncio.sleep(20)  # 20 saniye bekle
    await app.stop()

# Grup ID'si alma (örn. sen selam dediğinde)
@app.on_message(filters.text & filters.private)
async def get_group_id(client, message):
    chat_id = message.chat.id
    if chat_id not in GROUP_IDS:
        GROUP_IDS.append(chat_id)
        print(f"Yeni chat ID eklendi: {chat_id}")

asyncio.run(send_messages())
