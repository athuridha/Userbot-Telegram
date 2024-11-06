from telethon import events, errors
from telethon.tl.functions.channels import EditTitleRequest, EditPhotoRequest
from telethon.tl.functions.messages import EditChatTitleRequest
from telethon.tl.types import InputChatUploadedPhoto, ChatPhotoEmpty
from .utils import restricted_to_authorized
import io

def load(client):
    @client.on(events.NewMessage(pattern=r'\.gpinfo(?:\s+(.+))?'))
    @restricted_to_authorized
    async def group_info(event):
        try:
            group_identifier = event.pattern_match.group(1)

            # Jika ada argumen (username, link grup, atau ID grup), ambil entitas grupnya
            if group_identifier:
                try:
                    # Mengubah ID grup menjadi int jika group_identifier adalah angka
                    group_id = int(group_identifier) if group_identifier.isdigit() else group_identifier
                    group = await client.get_entity(group_id)
                except ValueError:
                    # Jika input bukan angka, gunakan langsung sebagai username/link grup
                    group = await client.get_entity(group_identifier)
            else:
                # Jika tidak ada argumen, gunakan chat ID dari event saat ini
                group = await event.get_chat()

            # Mendapatkan username grup atau "Tidak ada" jika username tidak tersedia
            if not group.username:
                username = "Tidak ada"
            else:
                username = f"@{group.username}"

            info = f"ℹ️ Informasi Grup:\n\n"
            info += f"🆔 ID: `{group.id}`\n"
            info += f"📝 Judul: `{group.title}`\n"
            info += f"🔗 Username: {username}\n"

            if hasattr(group, 'participants_count'):
                info += f"👥 Jumlah Anggota: {group.participants_count}\n"
            if hasattr(group, 'about'):
                info += f"ℹ️ Deskripsi: {group.about}\n"

            await event.reply(info)
        except Exception as e:
            await event.reply(f"❌ Terjadi kesalahan: {str(e)}")

def add_commands(add_command):
    add_command('.setgpic', 'Mengubah foto profil grup (balas ke sebuah foto)')
    add_command('.setgtitle [judul baru]', 'Mengubah judul grup')
    add_command('.setgdesc [deskripsi baru]', 'Mengubah deskripsi grup')
    add_command('.addgemoji [emoji]', 'Menambahkan emoji ke judul grup')
    add_command('.gpinfo [username/link/ID grup]', 'Menampilkan informasi tentang grup berdasarkan username, link, atau ID grup')
