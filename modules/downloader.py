from telethon import events
import youtube_dl
import asyncio
import os
from .utils import restricted_to_authorized

def get_user_download_dir(user_id):
    user_dir = f'downloads/user_{user_id}'
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return user_dir

def load(client):
    @client.on(events.NewMessage(pattern=r'\.yt (.+)'))
    @restricted_to_authorized
    async def youtube_download(event):
        url = event.pattern_match.group(1)
        user_id = event.sender_id
        user_dir = get_user_download_dir(user_id)
        ydl_opts = {'outtmpl': f'{user_dir}/%(title)s.%(ext)s'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                filename = ydl.prepare_filename(info)
                await event.reply(f"Mulai mengunduh: {info['title']}")
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, lambda: ydl.download([url]))
                await client.send_file(event.chat_id, filename, caption=info['title'])
                await event.reply("Download selesai!")
                os.remove(filename)  # Hapus file setelah dikirim
            except Exception as e:
                await event.reply(f"Gagal mengunduh: {str(e)}")

    @client.on(events.NewMessage(pattern=r'\.ig (.+)'))
    @restricted_to_authorized
    async def instagram_download(event):
        url = event.pattern_match.group(1)
        user_id = event.sender_id
        user_dir = get_user_download_dir(user_id)
        ydl_opts = {'outtmpl': f'{user_dir}/%(title)s.%(ext)s'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                filename = ydl.prepare_filename(info)
                await event.reply("Mulai mengunduh dari Instagram...")
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, lambda: ydl.download([url]))
                await client.send_file(event.chat_id, filename)
                await event.reply("Download selesai!")
                os.remove(filename)  # Hapus file setelah dikirim
            except Exception as e:
                await event.reply(f"Gagal mengunduh: {str(e)}")

def add_commands(add_command):
    add_command('.yt <url>', '📥 Mengunduh video dari YouTube')
    add_command('.ig <url>', '📥 Mengunduh media dari Instagram')