from telethon import events, functions, types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from .utils import restricted_to_authorized
import asyncio
import json
import os

WARNS_FILE = 'user_warns_{}.json'
MAX_WARNS = 3

# ID pemilik bot (owner), ganti dengan ID pemilik yang sebenarnya
OWNER_ID = 777208565  # Ganti dengan ID pemilik akun

def is_owner(user_id):
    """Memeriksa apakah user_id adalah pemilik bot"""
    return user_id == OWNER_ID

def load_warns(user_id):
    file_name = WARNS_FILE.format(user_id)
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            return json.load(f)
    return {}

def save_warns(user_id, warns):
    file_name = WARNS_FILE.format(user_id)
    with open(file_name, 'w') as f:
        json.dump(warns, f)

def load(client):
    @client.on(events.NewMessage(pattern=r'\.ban'))
    @restricted_to_authorized
    async def ban_user(event):
        sender = event.sender_id
        if not is_owner(sender):
            return await event.reply("❌ Hanya pemilik bot yang dapat menjalankan perintah ini.")

        if event.is_reply:
            reply = await event.get_reply_message()
            chat = await event.get_chat()
            try:
                permissions = await client.get_permissions(chat, event.sender_id)
                if not permissions.is_admin:
                    await event.edit("❌ Anda bukan admin di grup ini.")
                    return
                await client(EditBannedRequest(
                    channel=chat.id,
                    user_id=reply.sender_id,
                    banned_rights=ChatBannedRights(until_date=None, view_messages=True)
                ))
                await event.edit("✅ Pengguna berhasil dibanned.")
            except Exception as e:
                await event.edit(f"❌ Gagal melakukan ban: {str(e)}")
        else:
            await event.edit("🔔 Mohon balas ke pesan pengguna yang ingin di-ban.")

    @client.on(events.NewMessage(pattern=r'\.unban'))
    @restricted_to_authorized
    async def unban_user(event):
        sender = event.sender_id
        if not is_owner(sender):
            return await event.reply("❌ Hanya pemilik bot yang dapat menjalankan perintah ini.")

        if event.is_reply:
            reply = await event.get_reply_message()
            chat = await event.get_chat()
            try:
                permissions = await client.get_permissions(chat, event.sender_id)
                if not permissions.is_admin:
                    await event.edit("❌ Anda bukan admin di grup ini.")
                    return
                await client(EditBannedRequest(
                    channel=chat.id,
                    user_id=reply.sender_id,
                    banned_rights=ChatBannedRights(until_date=None, view_messages=False)
                ))
                await event.edit("✅ Pengguna berhasil di-unban.")
            except Exception as e:
                await event.edit(f"❌ Gagal melakukan unban: {str(e)}")
        else:
            await event.edit("🔔 Mohon balas ke pesan pengguna yang ingin di-unban.")

    @client.on(events.NewMessage(pattern=r'\.warn'))
    @restricted_to_authorized
    async def warn_user(event):
        sender = event.sender_id
        if not is_owner(sender):
            return await event.reply("❌ Hanya pemilik bot yang dapat menjalankan perintah ini.")

        if event.is_reply:
            reply = await event.get_reply_message()
            chat = await event.get_chat()
            user_id = str(reply.sender_id)
            chat_id = str(chat.id)

            permissions = await client.get_permissions(chat, event.sender_id)
            if not permissions.is_admin:
                await event.edit("❌ Anda bukan admin di grup ini.")
                return

            warns = load_warns(event.sender_id)
            if chat_id not in warns:
                warns[chat_id] = {}
            if user_id not in warns[chat_id]:
                warns[chat_id][user_id] = 0

            warns[chat_id][user_id] += 1
            warn_count = warns[chat_id][user_id]

            save_warns(event.sender_id, warns)

            if warn_count >= MAX_WARNS:
                try:
                    await client(EditBannedRequest(
                        channel=chat.id,
                        user_id=reply.sender_id,
                        banned_rights=ChatBannedRights(until_date=None, view_messages=True)
                    ))
                    await event.edit(f"⚠️ Pengguna telah mencapai batas peringatan ({MAX_WARNS}) dan telah dibanned.")
                    del warns[chat_id][user_id]
                    save_warns(event.sender_id, warns)
                except Exception as e:
                    await event.edit(f"❌ Gagal melakukan ban otomatis: {str(e)}")
            else:
                await event.edit(f"⚠️ Pengguna telah diberikan peringatan ({warn_count}/{MAX_WARNS}).")
        else:
            await event.edit("🔔 Mohon balas ke pesan pengguna yang ingin diberi peringatan.")

    @client.on(events.NewMessage(pattern=r'\.kicks'))
    @restricted_to_authorized
    async def kick_user(event):
        sender = event.sender_id
        if not is_owner(sender):
            return await event.reply("❌ Hanya pemilik bot yang dapat menjalankan perintah ini.")

        if event.is_reply:
            reply = await event.get_reply_message()
            chat = await event.get_chat()
            try:
                permissions = await client.get_permissions(chat, event.sender_id)
                if not permissions.is_admin:
                    await event.edit("❌ Anda bukan admin di grup ini.")
                    return
                await client.kick_participant(chat.id, reply.sender_id)
                await event.edit("👢 Pengguna berhasil dikeluarkan dari grup.")
            except Exception as e:
                await event.edit(f"❌ Gagal mengeluarkan pengguna: {str(e)}")
        else:
            await event.edit("🔔 Mohon balas ke pesan pengguna yang ingin dikeluarkan.")

    @client.on(events.NewMessage(pattern=r'\.mute'))
    @restricted_to_authorized
    async def mute_user(event):
        sender = event.sender_id
        if not is_owner(sender):
            return await event.reply("❌ Hanya pemilik bot yang dapat menjalankan perintah ini.")

        if event.is_reply:
            reply = await event.get_reply_message()
            chat = await event.get_chat()
            try:
                permissions = await client.get_permissions(chat, event.sender_id)
                if not permissions.is_admin:
                    await event.edit("❌ Anda bukan admin di grup ini.")
                    return
                await client(EditBannedRequest(
                    channel=chat.id,
                    user_id=reply.sender_id,
                    banned_rights=ChatBannedRights(until_date=None, send_messages=True)
                ))
                await event.edit("🔇 Pengguna berhasil di-mute.")
            except Exception as e:
                await event.edit(f"❌ Gagal melakukan mute: {str(e)}")
        else:
            await event.edit("🔔 Mohon balas ke pesan pengguna yang ingin di-mute.")

    @client.on(events.NewMessage(pattern=r'\.unmute'))
    @restricted_to_authorized
    async def unmute_user(event):
        sender = event.sender_id
        if not is_owner(sender):
            return await event.reply("❌ Hanya pemilik bot yang dapat menjalankan perintah ini.")

        if event.is_reply:
            reply = await event.get_reply_message()
            chat = await event.get_chat()
            try:
                permissions = await client.get_permissions(chat, event.sender_id)
                if not permissions.is_admin:
                    await event.edit("❌ Anda bukan admin di grup ini.")
                    return
                await client(EditBannedRequest(
                    channel=chat.id,
                    user_id=reply.sender_id,
                    banned_rights=ChatBannedRights(until_date=None, send_messages=False)
                ))
                await event.edit("🔊 Pengguna berhasil di-unmute.")
            except Exception as e:
                await event.edit(f"❌ Gagal melakukan unmute: {str(e)}")
        else:
            await event.edit("🔔 Mohon balas ke pesan pengguna yang ingin di-unmute.")

def add_commands(add_command):
    add_command('.ban', '🚫 Mem-ban pengguna dari grup (balas ke pesan pengguna)')
    add_command('.unban', '✅ Membatalkan ban pengguna dari grup (balas ke pesan pengguna)')
    add_command('.warn', '⚠️ Memberikan peringatan kepada pengguna (balas ke pesan pengguna)')
    add_command('.kicks', '👢 Mengeluarkan pengguna dari grup (balas ke pesan pengguna)')
    add_command('.mute', '🔇 Membisukan pengguna dalam grup (balas ke pesan pengguna)')
    add_command('.unmute', '🔊 Membatalkan bisukan pengguna dalam grup (balas ke pesan pengguna)')
