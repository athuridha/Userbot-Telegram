import os
import speech_recognition as sr
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from telethon import events
from .utils import restricted_to_authorized

if not os.path.exists("temp"):
    os.makedirs("temp")

def load(client):
    @client.on(events.NewMessage(pattern=r'\.transcribe'))
    @restricted_to_authorized
    async def transcribe_audio_video(event):
        if event.is_reply:
            replied = await event.get_reply_message()
            if replied.video or replied.document or replied.audio:
                await event.edit("🔄 Memulai proses transkripsi... Mohon tunggu, ini mungkin memakan waktu.")
                try:
                    file_path = await client.download_media(replied, "temp/")
                                        
                    if file_path.endswith(('.mp4', '.avi', '.mov', '.flv')):
                        video = VideoFileClip(file_path)
                        audio_path = "temp/extracted_audio.wav"
                        video.audio.write_audiofile(audio_path)
                        os.remove(file_path)
                        file_path = audio_path
                                        
                    if not file_path.endswith('.wav'):
                        audio = AudioSegment.from_file(file_path)
                        file_path_wav = file_path.rsplit('.', 1)[0] + '.wav'
                        audio.export(file_path_wav, format="wav")
                        os.remove(file_path)  
                        file_path = file_path_wav
                                        
                    recognizer = sr.Recognizer()
                    with sr.AudioFile(file_path) as source:
                        audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language="id-ID")
                                        
                    os.remove(file_path)
                                        
                    await event.edit(f"📝 Hasil transkripsi:\n\n{text}")
                except Exception as e:
                    await event.edit(f"❌ Terjadi kesalahan saat transkripsi: {str(e)}")
            else:
                await event.edit("❗ Mohon balas ke file audio atau video yang ingin ditranskripsikan.")
        else:
            await event.edit("❗ Mohon balas ke file audio atau video yang ingin ditranskripsikan.")

def add_commands(add_command):
    add_command('.transcribe', '🎙️ Mentranskripsikan audio dari file video atau audio (balas ke file)')