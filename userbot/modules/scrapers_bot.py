
import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot.events import register
from userbot import bot, CMD_HELP
from time import sleep
import os
from telethon.tl.types import MessageMediaPhoto
import asyncio
from userbot.modules.admin import get_user_from_event
from PIL import Image, ImageDraw, ImageFont
import textwrap
from userbot.cmdhelp import CmdHelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("scrapers_bot")

# ████████████████████████████████

def is_message_image(message):
    if message.media:
        if isinstance(message.media, MessageMediaPhoto):
            return True
        if message.media.document:
            if message.media.document.mime_type.split("/")[0] == "image":
                return True
        return False
    return False
    
async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response

def MemeYap (Resim, Text, FontS = 40, Bottom = False, BottomText = None):
    Foto = Image.open(Resim)
    Yazi = ImageDraw.Draw(Foto)
    FontSize = 20
    ImgFraction = float(f"0.{FontS}")

    Font = ImageFont.truetype("./userbot/fonts/impact.ttf", FontSize)
    while Font.getsize(Text)[0] < ImgFraction*Foto.size[0]:
        FontSize += 1
        Font = ImageFont.truetype("./userbot/fonts/impact.ttf", FontSize)
    FontSize -= 1
    Font = ImageFont.truetype("./userbot/fonts/impact.ttf", FontSize)

    def drawTextWithOutline(text, x, y):
        Yazi.text((x-2, y-2), text,(0,0,0),font=Font)
        Yazi.text((x+2, y-2), text,(0,0,0),font=Font)
        Yazi.text((x+2, y+2), text,(0,0,0),font=Font)
        Yazi.text((x-2, y+2), text,(0,0,0),font=Font)
        Yazi.text((x, y), text, (255,255,255), font=Font)
        return

    w, h = Yazi.textsize(Text, Font)
    Satirlar = textwrap.wrap(Text, width=22)
    lastY = -h

    for i in range(0, len(Satirlar)):
        w, h = Yazi.textsize(Satirlar[i], Font)
        x = Foto.width/2 - w/2
        y = i * h
        drawTextWithOutline(Satirlar[i], x, y)

        if Bottom:
            Bottom_Satirlar = textwrap.wrap(BottomText, width=22)
            lastY = Foto.height - h * (len(Bottom_Satirlar) +1) - 10

            for i in range(0, len(Bottom_Satirlar)):
                w, h = Yazi.textsize(Bottom_Satirlar[i], Font)
                x = Foto.width/2 - w/2
                y = lastY + h
                drawTextWithOutline(Bottom_Satirlar[i], x, y)
                lastY = y

    Foto.save("Lunameme.png")

@register(outgoing=True, pattern="^.sangmata(?: |$)(.*)")
async def sangmata(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit(LANG['REPLY_MSG'])
       return
    chat = "@SangMata_beta_bot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit(LANG['REPLY_BOT_ERROR'])
       return
    await event.edit(LANG['WORKING_ON'])
    async with bot.conversation(chat, exclusive=False) as conv:
          response = None
          try:
              msg = await reply_message.forward_to(chat)
              response = await conv.get_response(message=msg, timeout=5)
          except YouBlockedUserError: 
              await event.edit(LANG['BLOCKED_ERROR'])
              return
          except Exception as e:
              print(e.__class__)

          if not response:
              await event.edit(LANG['NOT_RESPONSE'])
          elif response.text.startswith("Forward"):
             await event.edit(LANG['USER_PRIVACY'])
          else: 
             await event.edit(response.text)
          sleep(1)
          await bot.send_read_acknowledge(chat, max_id=(response.id+3))
          await conv.cancel_all()

@register(outgoing=True, pattern="^.meme ?((\d*)(.*))")
async def memeyap(event):
    """ """
    font = event.pattern_match.group(2)
    if font == "":
        font = 35
    else:
        font = int(font)
    text = event.pattern_match.group(3)
    await event.edit(LANG['MEMING'])
    if event.is_reply:
        reply = await event.get_reply_message()
        if ";" in text:
            Split = text.split(";")
            Bottom = True
            Text = Split[0]
            BottomText = Split[1]
        else:
            Bottom = False
            Text = text
            BottomText = None
        
        if reply.photo:
            Resim = await reply.download_media()
        elif reply.sticker and reply.file.ext == ".webp":
            if os.path.exists("./LunaSticker.png"):
                os.remove("./LunaSticker.png")

            foto = await reply.download_media()
            im = Image.open(foto).convert("RGB")
            im.save("LunaSticker.png", "png")
            Resim = "LunaSticker.png"
        elif reply.sticker and reply.file.ext == ".tgs":
            sticker = await reply.download_media()
            os.system(f"lottie_convert.py --frame 0 -if lottie -of png '{sticker}' LunaSticker.png")
            os.remove(sticker)
            Resim = "LunaSticker.png"
        elif reply.media:
            Resim = await reply.download_media()
            Sure = os.system("ffmpeg -i '"+Resim+"' 2>&1 | grep Duration | awk '{print $2}' | tr -d , | awk -F ':' '{print ($3+$2*60+$1*3600)/2}'``")
            os.system(f"ffmpeg -i '{Resim}' -vcodec mjpeg -vframes 1 -an -f rawvideo -ss {Sure} LunaThumb.jpg")
            os.remove(Resim)
            Resim = 'LunaThumb.jpg'
        else:
            return await event.edit(LANG['REPLY_TO_MEME'])
            
        if os.path.exists("./Lunameme.png"):
            os.remove("./Lunameme.png")

        MemeYap(Resim, Text, font, Bottom, BottomText)
        await event.client.send_file(event.chat_id, "./Lunameme.png", reply_to=reply)
        await event.delete()
        os.remove(Resim)
    else:
        await event.edit(LANG['REPLY_TO_MEME'])


from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.events import register

LANG1 = {
    'REPLY_TO_MESSAGE': "⚠️ **Zəhmət olmasa bir fayla cavab verin!**",
    'REPLY_TO_FILE': "⚠️ **Fayla cavab verməlisiniz. Bu bir fayl deyil!**",
    'REPLY_USER_ERR': "⚠️ **Botlar üçün bu əmri istifadə edə bilməzsiniz.**",
    'BLOCKED_CHAT': "❌ **Dr.Web botunu bloklamısınız. Lütfən blokdan çıxarın və yenidən cəhd edin.**",
    'USER_PRIVACY': "⚠️ **Bu istifadəçi öz məxfiliyini qoruyur, fayl Dr.Web botuna göndərilə bilmədi.**",
    'WAIT_EDIT': "⏳ **Skan edilməsi üçün bir az gözləyin...**",
    'MIZAH_EXE': "🔍 **Fayl skan ediləcək, gözləyin...**",
    'SCAN_RESULT': "🛡 **Skan nəticəsi**",
    'SCANNING': "🔄 **Skan davam edir, gözləyin...**",
    'CLEAN': "✅ **Təhlükə aşkar edilmədi! Fayl təmizdir.**",
    'VIRUS_DETECTED': "⚠️ **Virus aşkar edildi! Təhlükəsiz olmaq üçün faylı silin.**"
}

@register(outgoing=True, pattern="^.scan$")
async def scan(event):
    if event.fwd_from:
        return 

    if not event.reply_to_msg_id:
        await event.edit(LANG1['REPLY_TO_MESSAGE'])
        return

    reply_message = await event.get_reply_message() 

    if not reply_message.media:
        await event.edit(LANG1['REPLY_TO_FILE'])
        return
    
    chat = "@DrWebBot"

    if reply_message.sender.bot:
        await event.edit(LANG1['REPLY_USER_ERR'])
        return

    await event.edit(LANG1['MIZAH_EXE'])
    
    async with event.client.conversation(chat) as conv:
        try:
            await event.client.forward_messages(chat, reply_message)
            response = await conv.get_response()
        except YouBlockedUserError:
            await event.reply(LANG1['BLOCKED_CHAT'])
            return
        except ValueError:
            await event.edit("✅ **Mesaj Dr.Web botuna göndərildi. Zəhmət olmasa @drwebbot a baxın.**")
            return

        if response.text.startswith("Forward"):
            await event.edit(LANG1['USER_PRIVACY'])
            return

        elif response.text.startswith("Select"):
            await event.client.send_message(chat, "English")
            await event.edit(LANG1['WAIT_EDIT'])

            try:
                await event.client.forward_messages(chat, reply_message)
                response = await conv.get_response()
            except ValueError:
                await event.edit(" **Mesajı Dr.Web botuna yönləndirmək mümkün olmadı.**")
                return
            
            await event.edit(f"**{LANG1['SCAN_RESULT']}:**\n{response.text}")

        elif response.text.startswith("Still"):
            await event.edit(LANG1['SCANNING'])

            response = await conv.get_response()
            if response.text.startswith("No threats"):
                await event.edit(LANG1['CLEAN'])
            else:
                await event.edit(f"**{LANG1['VIRUS_DETECTED']}**\n\nƏtraflı məlumat: {response.text}")
        else:
            await event.edit(f"**{LANG1['SCAN_RESULT']}:**\n{response.text}")
    


@register(outgoing=True, pattern="^.creation")
async def creation(event):
    if not event.reply_to_msg_id:
        await event.edit(LANG['REPLY_TO_MSG'])
        return
    reply_message = await event.get_reply_message() 
    if event.fwd_from:
        return 
    chat = "@creationdatebot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    await event.edit(LANG['CALCULATING_TIME'])
    async with event.client.conversation(chat) as conv:
        try:     
            await event.client.forward_messages(chat, reply_message)
        except YouBlockedUserError:
            await event.reply(f"`Mmmh deyəsən` {chat} `əngəlləmisən. Xaiş əngəldən çıxar.`")
            return
      
        response = conv.wait_event(events.NewMessage(incoming=True,from_users=747653812))
        response = await response
        if response.text.startswith("Looks"):
            await event.edit(LANG['PRIVACY_ERR'])
        else:
            await event.edit(f"**Məlumat hazırdı: **`{response.text.replace('**','')}`")


@register(outgoing=True, pattern="^.ocr2")
async def ocriki(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    chat = "@bacakubot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    await event.edit(LANG['READING'])
    async with event.client.conversation(chat) as conv:
        try:     
            await event.client.forward_messages(chat, reply_message)
        except YouBlockedUserError:
            await event.reply(f"`Mmmh deyəsən` {chat} `əngəlləmisən. Xaiş əngəldən çıxar.`")
            return
      
        response = conv.wait_event(events.NewMessage(incoming=True,from_users=834289439))
        response = await response
        if response.text.startswith("Please try my other cool bot:"):
            response = conv.wait_event(events.NewMessage(incoming=True,from_users=834289439))
            response = await response

        if response.text == "":
            await event.edit(LANG['OCR_ERROR'])
        else:
            await event.edit(f"**{LANG['SEE_SOMETHING']}: **`{response.text}`")

@register(outgoing=True, pattern="^.voicy")
async def voicy(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    chat = "@Voicybot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    await event.edit("`Səsə qulaq asılır... Məmmədağa muğagağa...`")
    async with event.client.conversation(chat) as conv:
        try:     
            await event.client.forward_messages(chat, reply_message)
        except YouBlockedUserError:
            await event.reply(f"`Mmmh deyəsən` {chat} `əngəlləmisən. Xaiş əngəldan çıxar.`")
            return
      
        response = conv.wait_event(events.MessageEdited(incoming=True,from_users=259276793))
        response = await response
        if response.text.startswith("__👋"):
            await event.edit(LANG['VOICY_LANG_ERR'])
        elif response.text.startswith("__👮"):
            await event.edit(LANG['VOICY_ERR'])
        else:
            await event.edit(f"**{LANG['HEAR_SOMETHING']}: **`{response.text}`")

@register(outgoing=True, pattern="^.q(?: |$)(.*)")
async def quotly(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.text:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    chat = "@QuotLyBot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await event.edit(LANG['REPLY_TO_MSG'])
       return
    await event.edit(LANG['QUOTING'])

    async with bot.conversation(chat, exclusive=False, replies_are_responses=True) as conv:
        response = None
        try:
            sayi = event.pattern_match.group(1)
            if len(sayi) == 1:
                sayi = int(sayi)
                i = 1
                mesajlar = [event.reply_to_msg_id]
                while i < sayi:
                    mesajlar.append(event.reply_to_msg_id + i)
                    i += 1
                msg = await event.client.forward_messages(chat, mesajlar, from_peer=event.chat_id)
            else:
                msg = await reply_message.forward_to(chat)
            response = await conv.wait_event(events.NewMessage(incoming=True,from_users=1031952739), timeout=10)
        except YouBlockedUserError: 
            await event.edit(LANG['UNBLOCK_QUOTLY'])
            return
        except asyncio.TimeoutError:
            await event.edit("`Botdan cavab ala bilmədim!`")
            return
        except ValueError:
            await event.edit(LANG['QUOTLY_VALUE_ERR'])
            return
            
        if not response:
            await event.edit("`Botdan cavab ala bilmədim!`")
        elif response.text.startswith("Salam!"):
            await event.edit(LANG['USER_PRIVACY'])
        else: 
            await event.delete()
            await response.forward_to(event.chat_id)
        await conv.mark_read()
        await conv.cancel_all()

CmdHelp('scrapers_bot').add_command(
    'sangmata', (LANG['SANG1']), (LANG['SANG2'])
).add_command(
    'scan', (LANG['DR1']), (LANG['DR2'])
).add_command(
    'meme', (LANG['MEME1']), (LANG['MEME2']), (LANG['MEME3'])
).add_command(
    'voicy', (LANG['VO1']), (LANG['VO2'])
).add_command(
    'q', (LANG['Q1']), (LANG['Q2'])
).add_command(
    'ocr2', (LANG['OCR1']), (LANG['OCR2'])
).add_command(
    'creation', (LANG['CR1']), (LANG['CR2'])
).add()
