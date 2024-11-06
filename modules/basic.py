from telethon import events
from .utils import restricted_to_authorized

def load(client):
    @client.on(events.NewMessage(pattern=r'\.start'))
    @restricted_to_authorized
    async def start_handler(event):
        await event.reply('Halo! Userbot telah aktif.')

    @client.on(events.NewMessage(pattern=r'\.echo (.+)'))
    @restricted_to_authorized
    async def echo_handler(event):
        message = event.pattern_match.group(1)
        await event.reply(f'Anda mengatakan: {message}')

def add_commands(add_command):
    add_command('.start', 'Memulai bot dan memeriksa statusnya')
    add_command('.echo <teks>', 'Mengulangi teks yang dimasukkan')