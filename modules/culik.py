from telethon import events, functions, types
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import RPCError
from .utils import restricted_to_authorized
import asyncio
from datetime import datetime, timedelta
import pytz
import re

# Mendapatkan zona waktu Jakarta
jakarta_tz = pytz.timezone('Asia/Jakarta')

# Flag untuk menghentikan proses penculikan
cancel_invite = False

async def invite_members(client, target_group_id, source_group_id, limit, event):
    global cancel_invite
    cancel_invite = False  # Reset cancel flag

    try:
        # Mendapatkan anggota dari grup sumber
        members = await client.get_participants(source_group_id, limit=limit)
        members_to_invite = [member for member in members if not member.bot]

        if len(members_to_invite) == 0:
            await event.reply("❌ Tidak ada anggota yang ditemukan untuk diculik.")
            return

        # Mendapatkan anggota yang sudah ada di grup target
        existing_members = await client.get_participants(target_group_id)
        existing_member_ids = [member.id for member in existing_members]

        target_group = await client.get_entity(target_group_id)
        source_group = await client.get_entity(source_group_id)

        for i in range(0, len(members_to_invite), 1):  # menculik satu per satu
            if cancel_invite:
                await event.reply("⚠️ Proses penculikan dibatalkan.")
                return

            member_to_invite = members_to_invite[i]

            if member_to_invite.id not in existing_member_ids:
                try:
                    await client(InviteToChannelRequest(target_group_id, [member_to_invite.id]))
                    await event.reply(
                        f"✅ Berhasil menculik {member_to_invite.first_name} "
                        f"(ID: {member_to_invite.id}) ke grup {target_group.title}."
                    )
                except RPCError as e:
                    # Cek apakah ada error yang berhubungan dengan "A wait of X seconds"
                    wait_time_match = re.search(r'A wait of (\d+) seconds is required', str(e))
                    if wait_time_match:
                        wait_time = int(wait_time_match.group(1))
                        hours = wait_time // 3600
                        minutes = (wait_time % 3600) // 60
                        seconds = wait_time % 60
                        time_str = []
                        if hours > 0:
                            time_str.append(f"{hours} jam")
                        if minutes > 0:
                            time_str.append(f"{minutes} menit")
                        if seconds > 0:
                            time_str.append(f"{seconds} detik")
                        wait_time_formatted = " ".join(time_str)
                        await event.reply(
                            f"❌ Tidak bisa menculik lebih lanjut. Batas penculikan tercapai. "
                            f"Harap tunggu {wait_time_formatted} sebelum mencoba lagi."
                        )
                        cancel_invite = True  # Batalkan proses secara otomatis
                        return
                    else:
                        await event.reply(
                            f"❌ Terjadi kesalahan saat menculik {member_to_invite.first_name} "
                            f"(ID: {member_to_invite.id}): {str(e)}"
                        )
            else:
                await event.reply(
                    f"🔍 {member_to_invite.first_name} "
                    f"(ID: {member_to_invite.id}) sudah berada di grup {target_group.title}."
                )
                # Jika anggota sudah ada di grup, lanjutkan tanpa menunggu
                continue

            if i < len(members_to_invite) - 1:
                # Hitung waktu penculikan berikutnya dalam zona waktu Jakarta
                next_invite_time = datetime.now(jakarta_tz) + timedelta(minutes=1)
                next_invite_time_str = next_invite_time.strftime("%H:%M:%S")
                
                await event.reply(
                    f"⏳ Menunggu 1 menit sebelum menculik anggota berikutnya... "
                    f"(perkiraan waktu penculikan berikutnya: {next_invite_time_str})"
                )
                await asyncio.sleep(60)  # Delay 1 menit

    except RPCError as e:
        await event.reply(f"❌ Terjadi kesalahan: {str(e)}")

def load(client):
    @client.on(events.NewMessage(pattern=r'\.culik (\d+) (\d+) (\d+)'))
    @restricted_to_authorized
    async def invite(event):
        if not event.is_group:
            await event.reply("❌ Perintah ini hanya dapat digunakan di grup.")
            return

        try:
            # Parse the command arguments
            args = event.pattern_match.groups()
            limit = int(args[0])
            source_group_id = int(args[1])
            target_group_id = int(args[2])
            
            # Mendapatkan entitas (nama grup)
            source_group = await client.get_entity(source_group_id)
            target_group = await client.get_entity(target_group_id)
            
            # Informasikan pengguna tentang proses dan delay, dengan menampilkan nama grup
            await event.reply(
                f"🔄 Mulai menculik hingga {limit} anggota\ndari grup "
                f"'{source_group.title}' (ID: {source_group_id})\nke grup '{target_group.title}' (ID: {target_group_id}).\n\n"
                f"Proses ini akan memakan waktu karena ada delay 1 menit antara setiap penculikan."
            )
            
            await invite_members(client, target_group_id, source_group_id, limit, event)
        except ValueError:
            await event.reply("⚠️ Argumen tidak valid. Gunakan `.culik <jumlah> <idgroup target> <idgroup sumber>`.")
        except Exception as e:
            await event.reply(f"❌ Terjadi kesalahan: {str(e)}")

    @client.on(events.NewMessage(pattern=r'\.cancelculik'))
    @restricted_to_authorized
    async def cancel_invite_command(event):
        global cancel_invite
        cancel_invite = True
        await event.reply("⚠️ Proses penculikan sedang dibatalkan.")

def add_commands(add_command):
    add_command('.culik', '🔗 menculik anggota dari satu grup ke grup lain dengan delay 1 menit antara setiap penculikan. Anggota yang sudah ada di grup target tidak akan diculik.')
    add_command('.cancelculik', '❌ Batalkan proses culik anggota yang sedang berjalan.')