from telethon import events, types
from .utils import restricted_to_authorized
import asyncio

# Global variable to store ongoing tagall tasks
tagall_task = None

def load(client):
    @client.on(events.NewMessage(pattern=r'\.tagall (.+)'))
    @restricted_to_authorized
    async def tagall(event):
        global tagall_task
        
        # Check if there's already a tagall task running
        if tagall_task is not None:
            await event.respond("❌ Tagall sudah berjalan. Ketik `.canceltag` untuk membatalkan.")
            return
        
        reason = event.pattern_match.group(1)  # Get the reason from the command
        await event.respond(f"🔔 Mulai menandai semua anggota dengan alasan: {reason}")
        
        # Task for tagging all members
        async def tag_members():
            try:
                # Get all members from the chat
                chat = await event.get_chat()
                if isinstance(chat, (types.Chat, types.Channel)):
                    participants = await client.get_participants(chat)
                    
                    mentions = []
                    for i, participant in enumerate(participants):
                        if not tagall_task:  # Check if task is canceled
                            break
                        
                        # Prepare mention format
                        mention = f"[{participant.first_name}](tg://user?id={participant.id})"
                        mentions.append(mention)
                        
                        # Send a message for every 5 participants
                        if len(mentions) == 5:
                            await event.respond(f"{reason}\n" + ", ".join(mentions))  # Join with comma
                            mentions = []  # Reset the mentions list
                            await asyncio.sleep(1)  # Add a delay to avoid spamming
                    
                    # Send any remaining mentions
                    if mentions:
                        await event.respond(f"{reason}\n" + ", ".join(mentions))  # Join with comma
                    
                    await event.respond("✅ Selesai menandai semua anggota.")
                else:
                    await event.respond("❌ Perintah ini hanya berfungsi di grup.")
            except Exception as e:
                await event.respond(f"❌ Terjadi kesalahan: {str(e)}")
        
        # Start the tagall task
        tagall_task = client.loop.create_task(tag_members())

    @client.on(events.NewMessage(pattern=r'\.canceltag'))
    @restricted_to_authorized
    async def cancel_tagall(event):
        global tagall_task
        
        if tagall_task is None:
            await event.respond("❌ Tidak ada proses tagall yang sedang berjalan.")
        else:
            # Cancel the ongoing tagall task
            tagall_task.cancel()
            tagall_task = None
            await event.respond("🛑 Proses tagall dibatalkan.")

def add_commands(add_command):
    add_command('.tagall <alasan>', '🔔 Menandai semua anggota di grup dengan alasan yang diberikan, 5 orang sekaligus')
    add_command('.canceltag', '🛑 Membatalkan proses tagall yang sedang berjalan')
