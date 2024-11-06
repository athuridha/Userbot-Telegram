from telethon import events
import io
import math
import urllib.request
from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import DocumentAttributeFilename
from .utils import restricted_to_authorized

def resize_image(img):
    maxsize = (512, 512)
    if (img.width and img.height) < 512:
        size1 = img.width
        size2 = img.height
        if img.width > img.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        img = img.resize(sizenew)
    else:
        img.thumbnail(maxsize)
    return img

def create_text_image(text):
    img = Image.new('RGB', (512, 512), color='white')
    d = ImageDraw.Draw(img)
    
    try:
        fnt = ImageFont.load_default()
    except:
        try:
            fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        except:
            fnt = ImageFont.load_default()
    
    def get_text_dimensions(text, font):
        bbox = d.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    w, h = get_text_dimensions(text, fnt)
    
    while w > 500 or h > 500:
        if hasattr(fnt, 'path'):
            fnt = ImageFont.truetype(fnt.path, fnt.size - 1)
        else:
            fnt = ImageFont.load_default()
        w, h = get_text_dimensions(text, fnt)
    
    x = (512 - w) / 2
    y = (512 - h) / 2
    
    d.text((x, y), text, font=fnt, fill='black')
    return img

def load(client):
    @client.on(events.NewMessage(pattern=r'\.sticker'))
    @restricted_to_authorized
    async def sticker_to_png(event):
        if event.is_reply:
            reply_message = await event.get_reply_message()
            if reply_message.sticker:
                if reply_message.sticker.mime_type == "application/x-tgsticker":
                    await event.reply("❌ Maaf, stiker animasi belum didukung.")
                    return
                sticker_image = io.BytesIO()
                await client.download_media(reply_message.sticker, sticker_image)
                sticker_image.seek(0)
                img = Image.open(sticker_image)
                png_image = io.BytesIO()
                img.save(png_image, "PNG")
                png_image.name = "sticker.png"
                png_image.seek(0)
                await client.send_file(event.chat_id, png_image, force_document=True, reply_to=reply_message.id)
            else:
                await event.reply("🔔 Mohon balas ke sebuah stiker.")
        else:
            await event.reply("🔔 Mohon balas ke sebuah stiker.")

    @client.on(events.NewMessage(pattern=r'\.stkr'))
    @restricted_to_authorized
    async def image_to_sticker(event):
        if event.is_reply:
            reply_message = await event.get_reply_message()
            if reply_message.photo or reply_message.document:
                image = io.BytesIO()
                await client.download_media(reply_message, image)
                image.seek(0)
                img = Image.open(image)
                img = resize_image(img)
                sticker_image = io.BytesIO()
                img.save(sticker_image, "WebP", quality=95)
                sticker_image.name = "sticker.webp"
                sticker_image.seek(0)
                await client.send_file(event.chat_id, sticker_image, force_document=False, reply_to=reply_message.id)
            else:
                await event.reply("🔔 Mohon balas ke sebuah gambar.")
        else:
            await event.reply("🔔 Mohon balas ke sebuah gambar.")

    @client.on(events.NewMessage(pattern=r'\.stkrurl (.+)'))
    @restricted_to_authorized
    async def url_to_sticker(event):
        url = event.pattern_match.group(1)
        try:
            response = urllib.request.urlopen(url)
            image = io.BytesIO(response.read())
            img = Image.open(image)
            img = resize_image(img)
            sticker_image = io.BytesIO()
            img.save(sticker_image, "WebP", quality=95)
            sticker_image.name = "sticker.webp"
            sticker_image.seek(0)
            await client.send_file(event.chat_id, sticker_image, force_document=False)
        except Exception as e:
            await event.reply(f"❌ Terjadi kesalahan: {str(e)}")

    @client.on(events.NewMessage(pattern=r'\.stkrtext (.+)'))
    @restricted_to_authorized
    async def text_to_sticker(event):
        text = event.pattern_match.group(1)
        image = create_text_image(text)
        sticker_image = io.BytesIO()
        image.save(sticker_image, "WebP", quality=95)
        sticker_image.name = "sticker.webp"
        sticker_image.seek(0)
        await client.send_file(event.chat_id, sticker_image, force_document=False)

def add_commands(add_command):
    add_command('.sticker', '🖼️ Mengonversi stiker menjadi gambar PNG')
    add_command('.stkr', '🔄 Mengonversi gambar menjadi stiker')
    add_command('.stkrurl <url>', '🌐 Membuat stiker dari URL gambar')
    add_command('.stkrtext <teks>', '✍️ Membuat stiker dari teks')