from telethon import events, types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from .utils import restricted_to_authorized
import asyncio
import json
import os

FLOOD_FILE = 'flood_settings_{}.json'
FLOOD_CHECK = {}

def load_flood_settings(chat_id):
    file_name = FLOOD_FILE.format(chat_id)
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            return json.load(f)
    return {"limit": 5, "enabled": False}

def save_flood_settings(chat_id, settings):
    file_name = FLOOD_FILE.format(chat_id)
    with open(file_name, 'w') as f:
        json.dump(settings, f)

def load(client):
    @client.on(events.NewMessage())
    async def check_flood(event):
        if event.is_private:
            return

        chat_id = event.chat_id
        sender_id = event.sender_id
        settings = load_flood_settings(chat_id)

        if not settings["enabled"]:
            return

        if chat_id not in FLOOD_CHECK:
            FLOOD_CHECK[chat_id] = {}

        if sender_id not in FLOOD_CHECK[chat_id]:
            FLOOD_CHECK[chat_id][sender_id] = {"count": 1, "time": event.date}
        else:
            if (event.date - FLOOD_CHECK[chat_id][sender_id]["time"]).seconds > 5:
                FLOOD_CHECK[chat_id][sender_id] = {"count": 1, "time": event.date}
            else:
                FLOOD_CHECK[chat_id][sender_id]["count"] += 1

        if FLOOD_CHECK[chat_id][sender_id]["count"] > settings["limit"]:
            try:
                await client(EditBannedRequest(
                    channel=chat_id,
                    user_id=sender_id,
                    banned_rights=ChatBannedRights(until_date=None, send_messages=True)
                ))
                await event.reply(f"⚠️ Pengguna telah dibatasi karena melakukan flood.")
                del FLOOD_CHECK[chat_id][sender_id]
            except Exception as e:
                await event.reply(f"❌ Gagal membatasi pengguna: {str(e)}")

    @client.on(events.NewMessage(pattern=r'\.setflood (\d+)'))
    @restricted_to_authorized
    async def set_flood(event):
        limit = int(event.pattern_match.group(1))
        chat_id = event.chat_id
        settings = load_flood_settings(chat_id)
        settings["limit"] = limit
        settings["enabled"] = True
        save_flood_settings(chat_id, settings)
        await event.reply(f"✅ Batas flood diatur ke {limit} pesan.")

    @client.on(events.NewMessage(pattern=r'\.getflood'))
    @restricted_to_authorized
    async def get_flood(event):
        chat_id = event.chat_id
        settings = load_flood_settings(chat_id)
        if settings["enabled"]:
            await event.reply(f"🔢 Batas flood saat ini: {settings['limit']} pesan.")
        else:
            await event.reply("❌ Antiflood tidak aktif.")

    @client.on(events.NewMessage(pattern=r'\.remflood'))
    @restricted_to_authorized
    async def remove_flood(event):
        chat_id = event.chat_id
        settings = load_flood_settings(chat_id)
        settings["enabled"] = False
        save_flood_settings(chat_id, settings)
        await event.reply("✅ Antiflood telah dinonaktifkan.")

def add_commands(add_command):
    add_command('.setflood <jumlah>', 'Mengatur batas flood')
    add_command('.getflood', 'Mendapatkan pengaturan flood saat ini')
    add_command('.remflood', 'Menonaktifkan antiflood')