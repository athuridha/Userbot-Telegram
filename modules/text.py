from telethon import events
import random
import string
from .utils import restricted_to_authorized

def load(client):
    @client.on(events.NewMessage(pattern=r'\.upper (.+)'))
    @restricted_to_authorized
    async def uppercase(event):
        text = event.pattern_match.group(1)
        await event.edit(f"🔠 {text.upper()}")

    @client.on(events.NewMessage(pattern=r'\.lower (.+)'))
    @restricted_to_authorized
    async def lowercase(event):
        text = event.pattern_match.group(1)
        await event.edit(f"🔡 {text.lower()}")

    @client.on(events.NewMessage(pattern=r'\.reverse (.+)'))
    @restricted_to_authorized
    async def reverse_text(event):
        text = event.pattern_match.group(1)
        await event.edit(f"🔄 {text[::-1]}")

    @client.on(events.NewMessage(pattern=r'\.count (.+)'))
    @restricted_to_authorized
    async def count_text(event):
        text = event.pattern_match.group(1)
        char_count = len(text)
        word_count = len(text.split())
        await event.edit(f"📊 Statistik Teks:\n"
                          f"📝 Karakter: {char_count}\n"
                          f"🔤 Kata: {word_count}")

    @client.on(events.NewMessage(pattern=r'\.replace (.+) \| (.+) \| (.+)'))
    @restricted_to_authorized
    async def replace_text(event):
        text = event.pattern_match.group(1)
        old = event.pattern_match.group(2)
        new = event.pattern_match.group(3)
        result = text.replace(old, new)
        await event.edit(f"🔄 Hasil penggantian:\n{result}")

    @client.on(events.NewMessage(pattern=r'\.randomcase (.+)'))
    @restricted_to_authorized
    async def randomcase(event):
        text = event.pattern_match.group(1)
        result = ''.join(random.choice([str.upper, str.lower])(c) for c in text)
        await event.edit(f"🎲 {result}")

    @client.on(events.NewMessage(pattern=r'\.mockcase (.+)'))
    @restricted_to_authorized
    async def mockcase(event):
        text = event.pattern_match.group(1)
        result = ''.join(c.upper() if i % 2 else c.lower() for i, c in enumerate(text))
        await event.edit(f"🤪 {result}")

    @client.on(events.NewMessage(pattern=r'\.encrypt (.+)'))
    @restricted_to_authorized
    async def encrypt_text(event):
        text = event.pattern_match.group(1)
        shift = 3  # Caesar cipher dengan pergeseran 3
        result = ''.join(chr((ord(char) - 97 + shift) % 26 + 97) if char.isalpha() else char for char in text.lower())
        await event.edit(f"🔐 Teks Terenkripsi:\n{result}")

    @client.on(events.NewMessage(pattern=r'\.decrypt (.+)'))
    @restricted_to_authorized
    async def decrypt_text(event):
        text = event.pattern_match.group(1)
        shift = 3  # Caesar cipher dengan pergeseran 3
        result = ''.join(chr((ord(char) - 97 - shift) % 26 + 97) if char.isalpha() else char for char in text.lower())
        await event.edit(f"🔓 Teks Terdekripsi:\n{result}")

    @client.on(events.NewMessage(pattern=r'\.generate (\d+)'))
    @restricted_to_authorized
    async def generate_text(event):
        length = int(event.pattern_match.group(1))
        if length > 500:
            await event.edit("❌ Panjang teks maksimum adalah 500 karakter.")
            return
        result = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
        await event.edit(f"🎲 Teks Acak Generated:\n{result}")

def add_commands(add_command):
    add_command('.upper <teks>', '🔠 Mengubah teks menjadi huruf besar')
    add_command('.lower <teks>', '🔡 Mengubah teks menjadi huruf kecil')
    add_command('.reverse <teks>', '🔄 Membalikkan urutan teks')
    add_command('.count <teks>', '📊 Menghitung jumlah karakter dan kata dalam teks')
    add_command('.replace <teks> | <lama> | <baru>', '🔄 Mengganti bagian teks')
    add_command('.randomcase <teks>', '🎲 Mengacak besar-kecil huruf dalam teks')
    add_command('.mockcase <teks>', '🤪 Membuat teks menjadi mOcKcAsE')
    add_command('.encrypt <teks>', '🔐 Mengenkripsi teks (Caesar cipher)')
    add_command('.decrypt <teks>', '🔓 Mendekripsi teks (Caesar cipher)')
    add_command('.generate <jumlah>', '🎲 Menghasilkan teks acak dengan panjang tertentu')