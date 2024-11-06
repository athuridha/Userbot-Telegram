from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from .utils import restricted_to_authorized
import asyncio

CHAT = "SangMata_beta_bot"

def load(client):
    @client.on(events.NewMessage(pattern=r'\.sgb(?:\s+(.*))?$'))
    @restricted_to_authorized
    async def sangmata_beta(event):
        """
        Mendapatkan riwayat nama pengguna menggunakan SangMata Beta.
        Penggunaan: .sgb <balas/user_id/username>
        """
        args = event.pattern_match.group(1)
        reply = await event.get_reply_message()
        
        if args:
            try:
                user_id = await client.get_peer_id(args)
            except ValueError:
                user_id = args
        elif reply:
            user_id = reply.sender_id
        else:
            return await event.reply("Gunakan perintah ini dengan balasan atau berikan Username/ID...")

        lol = await event.reply("Sedang memproses...")
        try:
            async with client.conversation(CHAT, timeout=15) as conv:
                await conv.send_message(f"/allhistory {user_id}")
                response = await conv.get_response()
                if response and "no data available" in response.text.lower():
                    await lol.edit("Tidak ada catatan yang ditemukan untuk pengguna ini.")
                elif str(user_id) in response.message:
                    await lol.edit(response.text)
        except YouBlockedUserError:
            return await lol.edit(f"Mohon buka blokir @{CHAT} dan coba lagi.")
        except asyncio.TimeoutError:
            await lol.edit("Bot tidak merespons dalam waktu yang ditentukan.")
        except Exception as ex:
            await lol.edit(f"Terjadi kesalahan: {str(ex)}")
        finally:
            await asyncio.sleep(2)
            await client.send_read_acknowledge(CHAT)

    @client.on(events.NewMessage(pattern=r'\.sgbinfo$'))
    @restricted_to_authorized
    async def sangmata_info(event):
        """
        Menampilkan informasi tentang modul SangMata Beta.
        """
        info_text = """
🔍 **SangMata Beta Info**

SangMata Beta adalah bot yang dapat melacak perubahan nama, username, dan foto profil pengguna Telegram.

**Penggunaan:**
• `.sgb <balas/user_id/username>` - Mendapatkan riwayat perubahan pengguna
• `.sgbinfo` - Menampilkan informasi ini

**Catatan:**
• Bot ini mungkin tidak selalu memiliki data untuk semua pengguna.
• Penggunaan berlebihan dapat menyebabkan pembatasan oleh bot.
"""
        await event.reply(info_text)

def add_commands(add_command):
    add_command('.sgb <balas/user_id/username>', 'Mendapatkan riwayat nama pengguna menggunakan SangMata Beta')
    add_command('.sgbinfo', 'Menampilkan informasi tentang modul SangMata Beta')