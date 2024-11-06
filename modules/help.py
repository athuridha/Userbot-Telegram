from telethon import events
from collections import defaultdict
from .utils import restricted_to_authorized

command_list = defaultdict(list)

def load(client):
    @client.on(events.NewMessage(pattern=r'\.help(?: (.+))?'))
    @restricted_to_authorized
    async def help_command(event):
        command = event.pattern_match.group(1)
        if command:
            await show_command_help(event, command)
        else:
            await show_all_commands(event)

    async def show_all_commands(event):
        total_commands = sum(len(commands) for commands in command_list.values())
        help_text = "📚 **Daftar Perintah Isaura UBot:**\n"
        help_text += f"💡 Total Perintah: {total_commands}\n\n"
        
        for module, commands in sorted(command_list.items()):
            if commands:
                help_text += f"**{module.capitalize()}**\n"
                for cmd, desc in commands:
                    short_desc = desc.split('.')[0]  # Take only the first sentence
                    help_text += f"  • `{cmd.ljust(15)}`: {short_desc}\n"
                help_text += "\n"
        
        help_text += "Gunakan `.help <perintah>` untuk informasi lebih detail tentang perintah tertentu."
        
        await send_long_message(event, help_text)

    async def show_command_help(event, command):
        for module, commands in command_list.items():
            for cmd, desc in commands:
                if cmd.split()[0] == command:
                    help_text = f"📌 **Perintah:** `{cmd}`\n"
                    help_text += f"📂 **Modul:** {module.capitalize()}\n"
                    help_text += f"📝 **Deskripsi:**\n{desc}"
                    await send_long_message(event, help_text)
                    return
        await event.reply(f"❌ Perintah '{command}' tidak ditemukan.")

    @client.on(events.NewMessage(pattern=r'\.listmodules'))
    @restricted_to_authorized
    async def list_modules(event):
        modules = sorted(command_list.keys())
        module_list = "📚 **Daftar Modul Isaura UBot:**\n\n"
        for module in modules:
            cmd_count = len(command_list[module])
            module_list += f"• **{module.capitalize().ljust(20)}** ({cmd_count} perintah)\n"
        module_list += "\nGunakan `.help <nama_modul>` untuk melihat perintah dalam modul tertentu."
        await send_long_message(event, module_list)

    @client.on(events.NewMessage(pattern=r'\.help (.+)'))
    @restricted_to_authorized
    async def module_help(event):
        module_name = event.pattern_match.group(1).lower()
        if module_name in command_list:
            help_text = f"📚 **Perintah dalam modul {module_name.capitalize()}:**\n\n"
            for cmd, desc in command_list[module_name]:
                help_text += f"• `{cmd.ljust(15)}`: {desc}\n\n"
            await send_long_message(event, help_text)
        else:
            await event.reply(f"❌ Modul '{module_name}' tidak ditemukan.")

    async def send_long_message(event, text):
        max_length = 4096
        if len(text) <= max_length:
            await event.reply(text)
        else:
            parts = []
            while len(text) > 0:
                if len(text) > max_length:
                    part = text[:max_length]
                    last_newline = part.rfind('\n')
                    if last_newline != -1:
                        parts.append(part[:last_newline])
                        text = text[last_newline+1:]
                    else:
                        parts.append(part)
                        text = text[max_length:]
                else:
                    parts.append(text)
                    text = ''
            
            for i, part in enumerate(parts):
                if i > 0:
                    part = f"(Lanjutan {i+1}/{len(parts)})\n\n" + part
                await event.reply(part)

def add_module_commands(add_command_func):
    module_name = add_command_func.__module__.split('.')[-1]
    add_command_func(lambda cmd, desc: command_list[module_name].append((cmd, desc)))

def add_commands(add_command):
    add_command('.help', '📚 Menampilkan daftar semua perintah')
    add_command('.help <perintah>', '🔍 Menampilkan informasi detail tentang perintah tertentu')
    add_command('.listmodules', '📂 Menampilkan daftar semua modul yang tersedia')
    add_command('.help <nama_modul>', '📚 Menampilkan semua perintah dalam modul tertentu')