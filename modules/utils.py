from telethon import events
from functools import wraps
import time
import math
import logging

logger = logging.getLogger(__name__)

# Mengelola pengguna yang diotorisasi per client
authorized_users = {}

def add_authorized_user(client_id, user):
    """Tambahkan pengguna yang diotorisasi untuk client tertentu."""
    if client_id not in authorized_users:
        authorized_users[client_id] = set()

    authorized_users[client_id].add(user.id)
    logger.info(f"Added authorized user: {user.id} ({user.first_name}) for client {client_id}")

def is_authorized(client_id, user_id):
    """Periksa apakah pengguna diotorisasi untuk client tertentu."""
    return client_id in authorized_users and user_id in authorized_users[client_id]

def restricted_to_authorized(func):
    @wraps(func)
    async def wrapper(event):
        sender = await event.get_sender()
        client_id = (await event.client.get_me()).id
        
        if sender and is_authorized(client_id, sender.id):
            logger.info(f"Authorized user {sender.id} executed command: {event.raw_text}")
            return await func(event)
        else:
            logger.warning(f"Unauthorized user {sender.id} attempted to execute command: {event.raw_text}")
            # Opsional: Balas dengan pesan jika bukan user yang diizinkan yang mencoba menggunakan perintah
            # await event.reply("Maaf, perintah ini hanya dapat digunakan oleh pengguna yang diizinkan.")
            return
    return wrapper

def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["d", "h", "m", "s"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time

def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"

def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " day(s), ") if days else "") + \
        ((str(hours) + " hour(s), ") if hours else "") + \
        ((str(minutes) + " minute(s), ") if minutes else "") + \
        ((str(seconds) + " second(s), ") if seconds else "") + \
        ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    return tmp[:-2]

def percentage(part, whole):
    return 100 * float(part)/float(whole)

def progress(current, total, message, start_time, client, chat_id, message_id):
    now = time.time()
    diff = now - start_time
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        progress_str = "[{0}{1}] {2}%\n".format(
            ''.join(["▰" for _ in range(math.floor(percentage / 10))]),
            ''.join(["▱" for _ in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2))

        tmp = progress_str + \
              "Progress: {0} of {1}\n" \
              "Speed: {2}/s\n" \
              "ETA: {3}\n".format(
                  humanbytes(current),
                  humanbytes(total),
                  humanbytes(speed),
                  time_formatter(estimated_total_time)
              )
        client.edit_message(chat_id, message_id, tmp + message)

def load(client):
    # Tidak ada yang perlu dimuat untuk modul utilitas
    pass

def add_commands(add_command):
    # Tidak ada perintah yang perlu ditambahkan untuk modul utilitas
    pass
