from telethon import events, functions, types
from telethon.tl.functions.users import GetFullUserRequest
from telethon.errors import RPCError
from .utils import restricted_to_authorized
import io

def load(client):
    @client.on(events.NewMessage(pattern=r'\.id'))
    @restricted_to_authorized
    async def get_id(event):
        if event.is_reply:
            replied_msg = await event.get_reply_message()
            user_id = replied_msg.sender_id
            chat_id = event.chat_id
            if replied_msg.forward:
                if replied_msg.forward.sender_id:
                    user_id = replied_msg.forward.sender_id
                if replied_msg.forward.chat_id:
                    chat_id = replied_msg.forward.chat_id
            await event.edit(f"👤 ID Pengguna: `{user_id}`\n💬 ID Obrolan: `{chat_id}`")
        else:
            await event.edit(f"💬 ID Obrolan: `{event.chat_id}`")

    @client.on(events.NewMessage(pattern=r'\.info'))
    @restricted_to_authorized
    async def info(event):
        try:
            if event.is_reply:
                replied_msg = await event.get_reply_message()
                try:
                    user = await client.get_entity(replied_msg.sender_id)
                except ValueError:
                    await event.edit("❌ Tidak dapat menemukan informasi pengguna.")
                    return
            else:
                user = await event.get_sender()
            
            if isinstance(user, types.User):
                try:
                    full_user = await client(GetFullUserRequest(user.id))
                    
                    info_text = f"ℹ️ **Informasi Pengguna:**\n\n"
                    info_text += f"👤 Nama Depan: {user.first_name}\n"
                    if user.last_name:
                        info_text += f"📛 Nama Belakang: {user.last_name}\n"
                    if user.username:
                        info_text += f"🔖 Nama Pengguna: @{user.username}\n"
                    info_text += f"🆔 ID Pengguna: `{user.id}`\n"
                    if hasattr(full_user, 'about') and full_user.about:
                        info_text += f"📝 Bio: {full_user.about}\n"
                    elif hasattr(full_user, 'full_user') and hasattr(full_user.full_user, 'about') and full_user.full_user.about:
                        info_text += f"📝 Bio: {full_user.full_user.about}\n"
                    info_text += f"🔗 Tautan Permanen: [Tautan](tg://user?id={user.id})\n"
                    
                    # Ambil foto profil
                    profile_photo = await client.download_profile_photo(user, bytes)
                    
                    if profile_photo:
                        photo = io.BytesIO(profile_photo)
                        photo.name = "profile_photo.jpg"
                        await client.send_file(event.chat_id, photo, caption=info_text)
                    else:
                        await event.edit(info_text)
                except RPCError as e:
                    await event.edit(f"❌ Tidak dapat mengambil informasi lengkap pengguna: {str(e)}")
            elif isinstance(user, (types.Chat, types.Channel)):
                info_text = f"ℹ️ **Informasi Obrolan:**\n\n"
                info_text += f"📢 Judul: {user.title}\n"
                info_text += f"🆔 ID Obrolan: `{user.id}`\n"
                if hasattr(user, 'username') and user.username:
                    info_text += f"🔖 Nama Pengguna: @{user.username}\n"
                if hasattr(user, 'participants_count'):
                    info_text += f"👥 Jumlah Anggota: {user.participants_count}\n"
                await event.edit(info_text)
            else:
                await event.edit("❓ Tidak dapat mengenali jenis entitas.")
        except Exception as e:
            await event.edit(f"❌ Terjadi kesalahan: {str(e)}")

    @client.on(events.NewMessage(pattern=r'\.chatinfo'))
    @restricted_to_authorized
    async def chatinfo(event):
        chat = await event.get_chat()
        if isinstance(chat, types.Chat) or isinstance(chat, types.Channel):
            info_text = f"ℹ️ **Informasi Obrolan:**\n\n"
            info_text += f"📢 Judul: {chat.title}\n"
            info_text += f"🆔 ID Obrolan: `{chat.id}`\n"
            if hasattr(chat, 'username') and chat.username:
                info_text += f"🔖 Nama Pengguna: @{chat.username}\n"
            if hasattr(chat, 'participants_count'):
                info_text += f"👥 Jumlah Anggota: {chat.participants_count}\n"
            if chat.admin_rights:
                info_text += "👑 Anda memiliki hak admin di obrolan ini.\n"
            await event.edit(info_text)
        else:
            await event.edit("❌ Perintah ini hanya berfungsi di grup dan channel.")

def add_commands(add_command):
    add_command('.id', '🆔 Menampilkan ID pengguna dan obrolan')
    add_command('.info', 'ℹ️ Menampilkan informasi pengguna atau obrolan dengan foto profil')
    add_command('.chatinfo', '💬 Menampilkan informasi obrolan saat ini')