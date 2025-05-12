import asyncio
from telethon import events
from userbot import BRAIN_CHECKER, WHITELIST
from userbot.events import register


@register(incoming=True, from_users=WHITELIST, pattern="^.ualive$")
async def _(q):
    await q.client.send_message(q.chat_id,"`❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️ 💻 Online`")
