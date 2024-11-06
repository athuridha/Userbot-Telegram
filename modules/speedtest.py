from telethon import events
import subprocess
import json
import asyncio
from .utils import restricted_to_authorized

def load(client):
    @client.on(events.NewMessage(pattern=r'\.speedtest'))
    @restricted_to_authorized
    async def speedtest_func(event):
        animation = [
            "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"
        ]
        message = await event.reply("Memulai Speedtest...")
        for i in range(3):  # Animasi awal
            for frame in animation:
                await message.edit(f"Memulai Speedtest {frame}")
                await asyncio.sleep(0.2)

        await message.edit("Menjalankan speedtest...")
        try:
            # Menggunakan Ookla Speedtest CLI dengan output JSON
            command = "speedtest --json"
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Animasi selama proses berjalan
            while True:
                if process.returncode is not None:
                    break
                for frame in animation:
                    await message.edit(f"Menjalankan Speedtest {frame}")
                    await asyncio.sleep(0.2)

            stdout, stderr = await process.communicate()
            
            if stderr:
                await message.edit(f"Terjadi kesalahan: {stderr.decode('utf-8')}")
                return
            
            # Parsing output JSON
            result_json = json.loads(stdout.decode('utf-8'))
            
            ping = result_json['ping']
            download = result_json['download'] / 1_000_000  # Convert to Mbps
            upload = result_json['upload'] / 1_000_000  # Convert to Mbps
            isp = result_json['client']['isp']
            server = result_json['server']['sponsor']
            
            result = "**Hasil Speedtest**\n\n"
            result += f"**ISP:** `{isp}`\n"
            result += f"**Server:** `{server}`\n"
            result += f"**Ping:** `{ping:.2f}` ms\n"
            result += f"**Download:** `{download:.2f}` Mbps\n"
            result += f"**Upload:** `{upload:.2f}` Mbps"
            
            await message.edit(result)
        except Exception as e:
            await message.edit(f"Terjadi kesalahan: {str(e)}")

def add_commands(add_command):
    add_command('.speedtest', 'Menjalankan tes kecepatan internet menggunakan Ookla Speedtest')