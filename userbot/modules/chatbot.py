# ❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️ Əkmə OĞLUMMM
from telethon import events
from userbot import bot, GRUP_ID
from userbot.modules.sql_helper import chatbot_sql as db
from userbot.events import register
from userbot.cmdhelp import CmdHelp
import random

@register(outgoing=True, pattern="^.chatbot (on|off)$")
async def acbagla(event):
    cmd = event.pattern_match.group(1)
    chat_id = event.chat_id

    if cmd == "on":
        db.aktiv_chat(chat_id)
        await event.edit("**ChatBot bu söhbət üçün aktiv edildi.**")
    elif cmd == "off":
        db.deaktiv_chat(chat_id)
        await event.edit("**ChatBot bu söhbət üçün deaktiv edildi.**")

@register(incoming=True, disable_errors=True)
async def chatbot_aktiv(event):
    chat_id = event.chat_id
    if chat_id in GRUP_ID:
        return
    user_id = event.sender_id
    if not db.aktivdir(chat_id):
        return

    mesaj = event.text.strip()

    if event.sender_id == (await bot.get_me()).id:
        return

    db.user_elave(user_id, mesaj)

    cavablar = db.cavab(mesaj)
    if cavablar:
        await event.reply(random.choice(cavablar))
    elif event.is_reply:
        cavablanan = await event.get_reply_message()
        if cavablanan and cavablanan.sender_id != (await bot.get_me()).id:
            orjinal = cavablanan.text.strip().lower()
            db.elave_et(orjinal, mesaj)
CmdHelp('chatbot').add_command(
    'chatbot', '<on/off>', 'Yazdığınız gruplarda ChatBot özəlliyini aktivləşdirər'
).add_info(
    '❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️ Məhsuludur'
).add()
