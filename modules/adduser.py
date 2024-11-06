from telethon import events, TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
from telethon.sessions import StringSession
import asyncio
import json
import os
from .utils import add_authorized_user, is_authorized

# API ID dan API Hash yang tetap
API_ID = 22306157
API_HASH = "f5fdf9130ed21d53dbe62cfc7010696d"

# Owner ID untuk validasi pengguna
OWNER_ID = 123456789  # Ganti dengan ID pemilik akun

# Variabel global untuk menyimpan status proses
pending_requests = {}

def load_config():
    """Load user configuration from config.json"""
    CONFIG_FILE = 'config.json'
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return []

def save_config(config):
    """Save user configuration to config.json"""
    CONFIG_FILE = 'config.json'
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def remove_user_from_config(telepon):
    """Menghapus pengguna dari konfigurasi"""
    configs = load_config()
    new_configs = [config for config in configs if config['telepon'] != telepon]
    if len(new_configs) == len(configs):
        return False  # Tidak ada pengguna dengan nomor telepon tersebut
    save_config(new_configs)
    return True

def is_owner(user_id):
    """Memeriksa apakah user_id adalah pemilik bot"""
    return user_id == OWNER_ID

async def tambah_pengguna(telepon):
    """Memulai proses penambahan pengguna baru dengan mengirimkan OTP"""
    try:
        client = TelegramClient(StringSession(), API_ID, API_HASH)
        await client.connect()

        if not await client.is_user_authorized():
            await client.send_code_request(telepon)
            return client, "OTP_NEEDED"

        string_sesi = StringSession.save(client.session)
        return client, string_sesi
    except Exception as e:
        return None, str(e)

async def verifikasi_otp(client, telepon, kode_otp):
    """Memverifikasi kode OTP yang dikirimkan ke nomor telepon"""
    try:
        await client.sign_in(telepon, kode_otp)
        string_sesi = StringSession.save(client.session)
        return string_sesi, None
    except PhoneCodeInvalidError:
        return None, "Kode OTP tidak valid. Silakan coba lagi."
    except SessionPasswordNeededError:
        return "2FA_NEEDED", None
    except Exception as e:
        return None, str(e)

async def verifikasi_2fa(client, kata_sandi):
    """Memverifikasi 2FA jika diaktifkan pada akun"""
    try:
        await client.sign_in(password=kata_sandi)
        string_sesi = StringSession.save(client.session)
        return string_sesi, None
    except Exception as e:
        return None, str(e)

async def interactive_add_user(event, client):
    """Fungsi interaktif untuk menambah pengguna baru melalui dialog di chat"""
    chat = event.chat_id
    sender = event.sender_id

    # Cek apakah user adalah owner
    if not is_owner(sender):
        return await client.send_message(chat, "Hanya pemilik bot yang dapat menambahkan pengguna.")

    pending_requests[chat] = True

    async def get_reply(message):
        """Fungsi untuk mendapatkan balasan dari pengguna di chat"""
        prompt = await client.send_message(chat, message)
        while pending_requests.get(chat, False):
            try:
                response = await client.get_messages(chat, limit=1)
                if response and response[0].sender_id == sender and response[0].id > prompt.id:
                    return response[0].text
            except Exception as e:
                print(f"Error in get_reply: {e}")
            await asyncio.sleep(1)
        return None

    try:
        await client.send_message(chat, "Proses penambahan akun baru dimulai. Silakan ikuti langkah-langkah berikut:")

        telepon = await get_reply("Balas pesan ini dengan nomor telepon (format: +62xxxxxxxxxx):")
        if telepon is None: return await client.send_message(chat, "Proses dibatalkan.")

        await client.send_message(chat, "Memproses... Mengirim kode OTP.")
        new_client, result = await tambah_pengguna(telepon)

        if result == "OTP_NEEDED":
            otp = await get_reply("Balas pesan ini dengan kode OTP yang telah dikirim ke nomor Anda:")
            if otp is None: return await client.send_message(chat, "Proses dibatalkan.")

            string_sesi, error = await verifikasi_otp(new_client, telepon, otp)
            if error:
                await client.send_message(chat, f"Error: {error}")
                return
            elif string_sesi == "2FA_NEEDED":
                pwd = await get_reply("Akun ini menggunakan 2FA. Balas pesan ini dengan kata sandi 2FA:")
                if pwd is None: return await client.send_message(chat, "Proses dibatalkan.")

                string_sesi, error = await verifikasi_2fa(new_client, pwd)
                if error:
                    await client.send_message(chat, f"Error: {error}")
                    return
        elif isinstance(result, str) and result.startswith("Error"):
            await client.send_message(chat, f"Terjadi kesalahan: {result}")
            return
        else:
            string_sesi = result

        add_user_to_config(API_ID, API_HASH, telepon, string_sesi)

        me = await new_client.get_me()
        add_authorized_user(me.id, new_client)

        asyncio.create_task(start_new_client(API_ID, API_HASH, string_sesi))

        await client.send_message(chat, "Akun baru berhasil ditambahkan dan diaktifkan!")
    except Exception as e:
        await client.send_message(chat, f"Terjadi kesalahan: {str(e)}")
        print(f"Error in interactive_add_user: {e}")
    finally:
        pending_requests.pop(chat, None)

async def remove_user(event, client):
    """Fungsi untuk menghapus pengguna yang sudah ada"""
    chat = event.chat_id
    sender = event.sender_id

    # Cek apakah user adalah owner
    if not is_owner(sender):
        return await client.send_message(chat, "Hanya pemilik bot yang dapat menghapus pengguna.")

    async def get_reply(message):
        prompt = await client.send_message(chat, message)
        while pending_requests.get(chat, False):
            try:
                response = await client.get_messages(chat, limit=1)
                if response and response[0].sender_id == sender and response[0].id > prompt.id:
                    return response[0].text
            except Exception as e:
                print(f"Error in get_reply: {e}")
            await asyncio.sleep(1)
        return None

    telepon = await get_reply("Balas pesan ini dengan nomor telepon yang ingin dihapus (format: +62xxxxxxxxxx):")
    if telepon is None:
        return await client.send_message(chat, "Proses dibatalkan.")

    if remove_user_from_config(telepon):
        await client.send_message(chat, f"Pengguna dengan nomor {telepon} berhasil dihapus dari konfigurasi.")
    else:
        await client.send_message(chat, f"Tidak ada pengguna dengan nomor {telepon} yang ditemukan.")

async def cancel_process(event, client):
    """Membatalkan proses penambahan akun yang sedang berlangsung"""
    chat = event.chat_id
    sender = event.sender_id

    # Cek apakah user adalah owner
    if not is_owner(sender):
        return await client.send_message(chat, "Hanya pemilik bot yang dapat membatalkan proses ini.")

    if chat in pending_requests:
        pending_requests[chat] = False
        await client.send_message(chat, "Proses penambahan akun dibatalkan.")
    else:
        await client.send_message(chat, "Tidak ada proses penambahan akun yang sedang berlangsung.")

def load(client):
    """Fungsi untuk memuat event handler saat modul dipanggil"""
    global add_user_to_config, start_new_client
    from main import add_user_to_config, start_new_client

    # Handler untuk perintah .adduser
    @client.on(events.NewMessage(pattern=r'\.adduser'))
    async def handle_adduser(event):
        await interactive_add_user(event, client)

    # Handler untuk perintah .removeuser
    @client.on(events.NewMessage(pattern=r'\.removeuser'))
    async def handle_removeuser(event):
        await remove_user(event, client)

    # Handler untuk perintah .canceluser
    @client.on(events.NewMessage(pattern=r'\.canceluser'))
    async def handle_cancel(event):
        await cancel_process(event, client)

def add_commands(add_command):
    """Menambahkan perintah adduser, removeuser, dan canceluser ke command list"""
    add_command('.adduser', 'Menambahkan akun Telegram baru ke userbot')
    add_command('.removeuser', 'Menghapus pengguna Telegram dari userbot')
    add_command('.canceluser', 'Membatalkan proses penambahan akun yang sedang berlangsung')
