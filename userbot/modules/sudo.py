from telethon import events

import asyncio
from userbot import SUDO_ID
from userbot.cmdhelp import CmdHelp
from userbot.events import register

@register(incoming=True, from_users=SUDO_ID, pattern="^.salive$")
async def _(q):
    await q.client.send_message(q.chat_id,"`[❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️](https://t.me/lunadestek)ＳＵＤＯ ✨`")

CmdHelp('sudo').add_command(
    'salive', None, 'SUDOnun aktiv olub olmadığını yoxlayar.'
).add()
