from telethon import events
from collections import defaultdict
from .utils import restricted_to_authorized

def load(client):
    @client.on(events.NewMessage(pattern=r'\.gpstats'))
    @restricted_to_authorized
    async def group_stats(event):
        if not event.is_group:
            await event.edit("❌ Perintah ini hanya bisa digunakan dalam grup.")
            return
        
        await event.edit("🔄 Menganalisis statistik grup... Ini mungkin memakan waktu.")
        
        messages = await client.get_messages(event.chat_id, limit=1000)
        user_message_count = defaultdict(int)
        media_count = 0
        
        for message in messages:
            user_message_count[message.sender_id] += 1
            if message.media:
                media_count += 1
        
        top_users = sorted(user_message_count.items(), key=lambda x: x[1], reverse=True)[:5]
        
        stats = "📊 Statistik Grup (1000 pesan terakhir):\n\n"
        stats += f"👥 Total Pengirim Pesan: {len(user_message_count)}\n"
        stats += f"📸 Total Pesan Media: {media_count}\n\n"
        stats += "🏆 Top 5 Pengirim Pesan:\n"
        
        for user_id, count in top_users:
            user = await client.get_entity(user_id)
            stats += f"• {user.first_name}: {count} pesan\n"
        
        await event.edit(stats)

def add_commands(add_command):
    add_command('.gpstats', '📊 Menampilkan statistik grup')