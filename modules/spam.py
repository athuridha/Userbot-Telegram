from telethon import events
import asyncio
import time
from .utils import restricted_to_authorized

spam_tracker = {}

MAX_SPAM_PER_MINUTE = 50

def check_spam_limit(user_id, count):
    current_time = time.time()
    
    if user_id not in spam_tracker:
        spam_tracker[user_id] = {'count': 0, 'last_reset': current_time}
        
    if current_time - spam_tracker[user_id]['last_reset'] > 60:
        spam_tracker[user_id] = {'count': 0, 'last_reset': current_time}
    
    if spam_tracker[user_id]['count'] + count > MAX_SPAM_PER_MINUTE:
        return False
    
    spam_tracker[user_id]['count'] += count
    return True

def load(client):
    @client.on(events.NewMessage(pattern=r'\.spam (\d+) (.+)'))
    @restricted_to_authorized
    async def spam(event):
        count = int(event.pattern_match.group(1))
        message = event.pattern_match.group(2)
                
        if not check_spam_limit(event.sender_id, count):
            await event.edit("⚠️ Anda telah mencapai batas spam. Mohon tunggu beberapa saat.")
            return

        await event.delete()  

        for _ in range(count):
            await event.respond(message)
            await asyncio.sleep(0.5)

    @client.on(events.NewMessage(pattern=r'\.tspam (.+)'))
    @restricted_to_authorized
    async def tspam(event):
        message = event.pattern_match.group(1)
                
        if not check_spam_limit(event.sender_id, len(message)):
            await event.edit("⚠️ Anda telah mencapai batas spam. Mohon tunggu beberapa saat.")
            return

        await event.delete()

        for letter in message:
            await event.respond(letter)
            await asyncio.sleep(0.5)

    @client.on(events.NewMessage(pattern=r'\.wspam (.+)'))
    @restricted_to_authorized
    async def wspam(event):
        message = event.pattern_match.group(1)
        words = message.split()        
        
        if not check_spam_limit(event.sender_id, len(words)):
            await event.edit("⚠️ Anda telah mencapai batas spam. Mohon tunggu beberapa saat.")
            return

        await event.delete() 

        for word in words:
            await event.respond(word)
            await asyncio.sleep(0.5)

    @client.on(events.NewMessage(pattern=r'\.delayspam (\d+) (\d+) (.+)'))
    @restricted_to_authorized
    async def delayspam(event):
        delay = float(event.pattern_match.group(1))
        count = int(event.pattern_match.group(2))
        message = event.pattern_match.group(3)
        
        if not check_spam_limit(event.sender_id, count):
            await event.edit("⚠️ Anda telah mencapai batas spam. Mohon tunggu beberapa saat.")
            return

        await event.delete() 

        for _ in range(count):
            await event.respond(message)
            await asyncio.sleep(delay)

    @client.on(events.NewMessage(pattern=r'\.cancelspam'))
    @restricted_to_authorized
    async def cancel_spam(event):
        user_id = event.sender_id
        if user_id in spam_tracker:
            del spam_tracker[user_id]
            await event.edit("✅ Semua operasi spam telah dibatalkan.")
        else:
            await event.edit("❌ Tidak ada operasi spam yang sedang berjalan.")

def add_commands(add_command):
    add_command('.spam <jumlah> <pesan>', '🔁 Mengirim pesan berulang kali')
    add_command('.tspam <pesan>', '🔤 Mengirim setiap karakter dalam pesan sebagai pesan terpisah')
    add_command('.wspam <pesan>', '📝 Mengirim setiap kata dalam pesan sebagai pesan terpisah')
    add_command('.delayspam <delay> <jumlah> <pesan>', '⏱️ Mengirim pesan berulang kali dengan jeda waktu')
    add_command('.cancelspam', '🛑 Membatalkan semua operasi spam yang sedang berjalan')