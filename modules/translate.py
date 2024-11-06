from telethon import events
from googletrans import Translator, LANGUAGES
import emoji
from .utils import restricted_to_authorized

translator = Translator()

def remove_emoji(text):
    return emoji.replace_emoji(text, replace='')

def load(client):
    @client.on(events.NewMessage(pattern=r'\.tr(?: |$)(.*)'))
    @restricted_to_authorized
    async def translate_handler(event):
        if event.is_reply:
            replied = await event.get_reply_message()
            text = replied.text
        else:
            text = event.pattern_match.group(1)
        
        if not text:
            await event.edit("🔍 Mohon berikan teks untuk diterjemahkan atau balas ke pesan yang ingin diterjemahkan.")
            return

        try:
            detected = translator.detect(remove_emoji(text))
            src_lang = detected.lang
            
            # Selalu terjemahkan ke Bahasa Indonesia
            dest_lang = 'id'
          
            translation = translator.translate(text, dest=dest_lang, src=src_lang)
            
            result = f"🔤 **Dari:** {LANGUAGES.get(src_lang, 'Unknown').title()} ({src_lang})\n"
            result += f"🔤 **Ke:** {LANGUAGES.get(dest_lang, 'Unknown').title()} ({dest_lang})\n\n"
            result += f"📝 **Teks Asli:**\n{text}\n\n"
            result += f"🔄 **Terjemahan:**\n{translation.text}"
            
            await event.edit(result)
        except Exception as e:
            await event.edit(f"❌ Gagal menerjemahkan: {str(e)}")

def add_commands(add_command):
    add_command('.tr <teks>', '🔄 Mendeteksi bahasa dan menerjemahkan teks ke Bahasa Indonesia')