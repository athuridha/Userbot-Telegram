from telethon import events
import time
import json
import os
import asyncio
from .utils import restricted_to_authorized

AFK_FILE = 'afk_status_{}.json'

def format_time(seconds):
    intervals = (
        ('years', 31536000),  # 60 * 60 * 24 * 365
        ('weeks', 604800),    # 60 * 60 * 24 * 7
        ('days', 86400),      # 60 * 60 * 24
        ('hours', 3600),      # 60 * 60
        ('minutes', 60),
        ('seconds', 1)
    )
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append(f"{value} {name}")
    
    if len(result) > 1:
        return f"{', '.join(result[:-1])} and {result[-1]}"
    elif result:
        return result[0]
    else:
        return "just now"

def load_afk_status(user_id):
    file_name = AFK_FILE.format(user_id)
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            return json.load(f)
    return None

def save_afk_status(user_id, status):
    file_name = AFK_FILE.format(user_id)
    with open(file_name, 'w') as f:
        json.dump(status, f)

def remove_afk_status(user_id):
    file_name = AFK_FILE.format(user_id)
    if os.path.exists(file_name):
        os.remove(file_name)

def check_afk_status(user_id):
    status = load_afk_status(user_id)
    if status:
        return True, status
    return False, None

def load(client):
    @client.on(events.NewMessage(pattern=r'(?i)^\.afk(?: (.+))?'))
    @restricted_to_authorized
    async def afk_handler(event):
        reason = event.pattern_match.group(1)
        user = await event.get_sender()
        user_id = user.id
        first_name = user.first_name if user.first_name else "You"
        
        afk_status = {
            'time': time.time(),
            'name': first_name,
            'reason': reason if reason else None
        }
        save_afk_status(user_id, afk_status)

        if reason:
            await event.edit(f"{first_name} is now AFK. Reason: {reason}.")
        else:
            await event.edit(f"{first_name} is now AFK.")

        await asyncio.sleep(1)

    @client.on(events.NewMessage(outgoing=True))
    async def afk_responder(event):
        sender = await event.get_sender()
        is_afk, afk_status = check_afk_status(sender.id)
        
        if is_afk:
            # Ignore if the message is the .afk command
            if event.text and event.text.lower().startswith('.afk'):
                return
            
            afk_time = time.time() - afk_status['time']
            time_str = format_time(afk_time)
            name = afk_status['name']
            
            if afk_status['reason']:
                await event.respond(f"{name} is no longer AFK.\nReason was: {afk_status['reason']}\nAFK duration: {time_str}.")
            else:
                await event.respond(f"{name} is no longer AFK.\nAFK duration: {time_str}.")

            # Remove AFK status after responding
            remove_afk_status(sender.id)

    @client.on(events.NewMessage(incoming=True))
    async def mention_afk_responder(event):
        # Check if the message is a private message or if the user is mentioned
        if event.is_private or (event.mentioned and not event.from_users):
            # Get the receiver (AFK user) of the message
            if event.is_private:
                receiver = await event.get_chat()
            else:
                entities = await event.get_participants()
                receiver = next((entity for entity in entities if entity.mentioned), None)

            if receiver:
                is_afk, afk_status = check_afk_status(receiver.id)
                
                if is_afk:
                    afk_time = time.time() - afk_status['time']
                    time_str = format_time(afk_time)
                    name = afk_status['name']
                    
                    if afk_status['reason']:
                        response = f"{name} is currently AFK.\nReason: {afk_status['reason']}\nAFK for {time_str}."
                    else:
                        response = f"{name} is currently AFK.\nAFK for {time_str}."
                    
                    await event.reply(response)

def add_commands(add_command):
    add_command('.afk [reason]', 'Inform others that you are AFK')