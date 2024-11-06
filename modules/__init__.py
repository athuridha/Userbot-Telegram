import os
import importlib
from .utils import add_authorized_user

def load_modules(client):
    modules_dir = os.path.dirname(__file__)
    modules = []

    # Iterasi melalui semua file dalam direktori modules
    for filename in os.listdir(modules_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]  # Hilangkan .py dari nama file
            module = importlib.import_module(f'.{module_name}', package=__package__)
            
            if hasattr(module, 'load'):
                module.load(client)
                modules.append(module)
                print(f"Modul {module_name} berhasil dimuat.")
            
            if hasattr(module, 'add_commands'):
                from . import help
                help.add_module_commands(module.add_commands)

    print(f"Total {len(modules)} modul berhasil dimuat.")

    # Load help module terakhir
    from . import help
    help.load(client)

# Fungsi ini bisa dipanggil dari main.py untuk memulai proses pemuatan
def initialize(client):
    load_modules(client)