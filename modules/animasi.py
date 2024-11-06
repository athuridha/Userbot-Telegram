from telethon import events
from .utils import restricted_to_authorized
import asyncio

def load(client):
    """
    Fungsi ini akan memuat command untuk setiap instance client Telegram secara terpisah.
    """
    
    # Command untuk animasi cinta
    @client.on(events.NewMessage(pattern=r'\.loveu'))
    @restricted_to_authorized
    async def animate_loveu(event):
        e = await event.reply("I LOVEE YOUUU 💕")
        
        messages = [
            "💝💘💓💗",
            "💞💕💗💘",
            "💝💘💓💗",
            "💞💕💗💘",
            "💘💞💗💕",
            "💘💞💕💗",
            "SAYANG KAMU 💝💖💘",
            "💝💘💓💗",
            "💞💕💗💘",
            "💘💞💕💗",
            "SAYANG",
            "KAMU",
            "SELAMANYA 💕",
            "💘💘💘💘",
            "SAYANG",
            "KAMU",
            "SAYANG",
            "KAMU",
            "I LOVE YOUUUU",
            "MY BABY",
            "💕💞💘💝",
            "💘💕💞💝",
            "SAYANG KAMU💞"
        ]

        for message in messages:
            await e.edit(message)
            await asyncio.sleep(1)  # Tunggu 1 detik sebelum mengedit pesan berikutnya

    # Command untuk animasi hehe
    @client.on(events.NewMessage(pattern=r'\.hehe'))
    @restricted_to_authorized
    async def animate_hehe(event):
        typew = await event.reply(
            "`\n(\\_/)`" "`\n(●_●)`" "`\n />💖 *Ini Buat Kamu`"
        )
        await asyncio.sleep(2)
        await typew.edit(
            "`\n(\\_/)`" "`\n(●_●)`" "`\n💖<\\  *Tapi Bo'ong`"
        )

    # Command untuk animasi "I LOVE YOU"
    @client.on(events.NewMessage(pattern=r'\.ily'))
    @restricted_to_authorized
    async def animate_ily(event):
        e = await event.reply("💌 I 💖 LOOOVE 💖 YOU 💌")
        
        animations = [
            "💖 I 💖 LOOOVE 💖 YOU 💖",
            "💖 I 💗 LOOOVE 💗 YOU 💖",
            "💘 I 💝 LOOOVE 💝 YOU 💘",
            "💝 I 💖 LOOOVE 💖 YOU 💝",
            "💞 I 💕 LOOOVE 💕 YOU 💞",
            "💘 I 💓 LOOOVE 💓 YOU 💘",
            "💖 I 💖 LOOOVE 💖 YOU 💖",
            "💗 I 💘 LOOOVE 💘 YOU 💗",
            "💝 I 💗 LOOOVE 💗 YOU 💝",
            "💘 I 💖 LOOOVE 💖 YOU 💘",
            "💝 I 💝 LOOOVE 💝 YOU 💝",
            "💞 I 💕 LOOOVE 💕 YOU 💞",
            "💖 I 💖 LOOOVE 💖 YOU 💖",
            "💌 I 💖 LOOOVE 💖 YOU 💌",
            "💌 I 💖 YOU 💌",
            "💕 YOU 💕",
            "💖 LOOOVE 💖",
            "💌 I 💖 YOU 💌"
        ]

        for message in animations:
            await e.edit(message)
            await asyncio.sleep(1)  # Tunggu 1 detik sebelum mengedit pesan berikutnya

def add_commands(add_command):
    """
    Fungsi ini menambahkan command ke client.
    """
    add_command('.loveu', '🔄 Menampilkan animasi teks dengan berbagai pesan')
    add_command('.hehe', '🎭 Menampilkan animasi lucu dengan pesan')
    add_command('.ily', '💌 Menampilkan animasi teks "I LOVE YOU" dengan berbagai pesan')
