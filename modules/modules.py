import os
import importlib
import json
from telethon import events
from .utils import add_authorized_user, restricted_to_authorized

MODULE_STATUS_FILE = 'module_status.json'

def load_module_status():
    if os.path.exists(MODULE_STATUS_FILE):
        with open(MODULE_STATUS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_module_status(status):
    with open(MODULE_STATUS_FILE, 'w') as f:
        json.dump(status, f, indent=2)

def load_modules(client):
    modules_dir = os.path.dirname(__file__)
    modules = []
    module_status = load_module_status()

    for filename in os.listdir(modules_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            if module_status.get(module_name, True):  # Aktif secara default
                module = importlib.import_module(f'.{module_name}', package=__package__)
                
                if hasattr(module, 'load'):
                    module.load(client)
                    modules.append(module)
                    print(f"Modul {module_name} berhasil dimuat.")
                
                if hasattr(module, 'add_commands'):
                    from . import help
                    help.add_module_commands(module.add_commands)
            else:
                print(f"Modul {module_name} dinonaktifkan dan tidak dimuat.")

    print(f"Total {len(modules)} modul aktif berhasil dimuat.")

    # Load help module terakhir
    from . import help
    help.load(client)

def initialize(client):
    load_modules(client)
    
    @client.on(events.NewMessage(pattern=r'\.module (enable|disable) (\w+)'))
    @restricted_to_authorized
    async def manage_module(event):
        action, module_name = event.pattern_match.groups()
        module_status = load_module_status()
        
        if module_name not in module_status:
            module_status[module_name] = True
        
        if action == 'enable':
            module_status[module_name] = True
            message = f"Modul {module_name} berhasil diaktifkan. Silakan restart bot untuk menerapkan perubahan."
        else:
            module_status[module_name] = False
            message = f"Modul {module_name} berhasil dinonaktifkan. Silakan restart bot untuk menerapkan perubahan."
        
        save_module_status(module_status)
        await event.reply(message)
    
    @client.on(events.NewMessage(pattern=r'\.modules'))
    @restricted_to_authorized
    async def list_modules(event):
        module_status = load_module_status()
        modules_dir = os.path.dirname(__file__)
        
        message = "Daftar Modul:\n\n"
        for filename in os.listdir(modules_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                status = "Aktif" if module_status.get(module_name, True) else "Nonaktif"
                message += f"• {module_name}: {status}\n"
        
        await event.reply(message)

def add_commands(add_command):
    add_command('.module enable <nama_modul>', 'Mengaktifkan modul')
    add_command('.module disable <nama_modul>', 'Menonaktifkan modul')
    add_command('.modules', 'Menampilkan daftar modul dan statusnya')