from telethon import events
import time
from .utils import restricted_to_authorized

def load(client):
    @client.on(events.NewMessage(pattern=r'\.ping'))
    @restricted_to_authorized
    async def ping(event):
        start = time.time()
        message = await event.edit("Pong!")
        end = time.time()
        duration = (end - start) * 1000
        
        # Hanya menampilkan ping
        ping_result = f"**🏓 Ping:** `{duration:.2f}ms`"
        await message.edit(ping_result)

def add_commands(add_command):
    add_command('.ping', 'Menampilkan ping dalam milidetik')
