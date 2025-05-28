import asyncio
from telethon import events
from userbot import BRAIN_CHECKER, WHITELIST
from userbot.events import register


@register(incoming=True, from_users=WHITELIST, pattern="^.ualive$")
async def _(q):
    await q.client.send_message(q.chat_id,"`💠 𝐋𝐮𝐧𝐚𝐔𝐬𝐞𝐫𝐛𝐨𝐭 💠 💻 Online`")
