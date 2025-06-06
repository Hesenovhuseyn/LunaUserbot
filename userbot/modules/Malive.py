### Reponu öz adına çıxaran @HuseynH ata desin


from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import uname
from shutil import which
from os import remove
from userbot import LUNA_VERSION
from userbot import LUNA_USER, CMD_HELP
from telethon.tl.patched import Message
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR
from telethon import version
from platform import python_version
from userbot.cmdhelp import CmdHelp
from userbot.language import get_value

LANG = get_value("malive")


@register(outgoing=True, pattern="^.malive$")
async def malive(event):
    img = PLUGIN_MESAJLAR['malive']  
    caption = (
        "╭━━━➤ 『 BOT STATUS 』\n"
        f"┣• {LANG['ALIVE1']}\n"
        f"┣• {LANG['OK']}\n"
        "╰━━━━━━━━━━━━━━━━━━━\n\n"
        f"╭━━━➤ 『 {LANG['INFO']} 』\n"
        f"┣• 👤 {LANG['NAME']}: {LUNA_USER}\n"
        f"┣• ⚙️ {LANG['PYTHON']}: `{python_version()}`\n"
        f"┣• 🛠️ {LANG['VERSION']}: `{LUNA_VERSION}`\n"
        f"┣• 📚 {LANG['PLUGIN_COUNT']}: `{len(CMD_HELP)}`\n"
        "╰━━━━━━━━━━━━━━━━━━━\n\n"
        "#LunaUserbot"
    )
    await event.client.send_file(event.chat_id, img, caption=caption)
    await event.delete()

CmdHelp('malive').add_command('malive', None, 'LunaUserbotun aktivlik yoxlanması.'
).add_sahib(
    "[HUSEYN](t.me/huseynh) tərəfindən hazırlanmışdır"
).add()