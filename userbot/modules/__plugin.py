

import re
import os
from os.path import exists
from telethon.tl.types import DocumentAttributeFilename, InputMessagesFilterDocument
import importlib
import time
import traceback

from userbot import bot, TEHLUKELI, PLUGIN_CHANNEL_ID, PATTERNS
from userbot import tgbot, CMD_HELP
from userbot.events import register
from userbot.main import extractCommands
import userbot.cmdhelp

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("__plugin")

# ████████████████████████████████ #

# Plugin
@register(outgoing=True, pattern="^.pport")
async def pport(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
    else:
        await event.edit(LANG["REPLY_FOR_PORT"])
        return

    await event.edit(LANG["DOWNLOADING"])
    dosya = await event.client.download_media(reply_message)
    dosy = open(dosya, "r").read()

    borg1 = r"(@borg\.on\(admin_cmd\(pattern=\")(.*)(\")(\)\))"
    borg2 = r"(@borg\.on\(admin_cmd\(pattern=r\")(.*)(\")(\)\))"
    borg3 = r"(@borg\.on\(admin_cmd\(\")(.*)(\")(\)\))"

    if re.search(borg1, dosy):
        await event.edit(LANG["UNIBORG"])
        komu = re.findall(borg1, dosy)

        if len(komu) > 1:
            await event.edit(LANG["TOO_MANY_PLUGIN"])

        komut = komu[0][1]
        degistir = dosy.replace('@borg.on(admin_cmd(pattern="' + komut + '"))', '@register(outgoing=True, pattern="^.' + komut + '")')
        degistir = degistir.replace("from userbot.utils import admin_cmd", "from userbot.events import register")
        degistir = re.sub(r"(from uniborg).*", "from userbot.events import register", degistir)
        degistir = degistir.replace("def _(event):", "def port_" + komut + "(event):")
        degistir = degistir.replace("borg.", "event.client.")
        ported = open(f'port_{dosya}', "w").write(degistir)

        await event.edit(LANG["UPLOADING"])

        await event.client.send_file(event.chat_id, f"port_{dosya}")
        os.remove(f"port_{dosya}")
        os.remove(f"{dosya}")
    elif re.search(borg2, dosy):
        await event.edit(LANG["UNIBORG2"])
        komu = re.findall(borg2, dosy)

        if len(komu) > 1:
            await event.edit(LANG["TOO_MANY_PLUGIN"])
            return

        komut = komu[0][1]

        degistir = dosy.replace('@borg.on(admin_cmd(pattern=r"' + komut + '"))', '@register(outgoing=True, pattern="^.' + komut + '")')
        degistir = degistir.replace("from userbot.utils import admin_cmd", "from userbot.events import register")
        degistir = re.sub(r"(from uniborg).*", "from userbot.events import register", degistir)
        degistir = degistir.replace("def _(event):", "def port_" + komut + "(event):")
        degistir = degistir.replace("borg.", "event.client.")
        ported = open(f'port_{dosya}', "w").write(degistir)

        await event.edit(LANG["UPLOADING"])

        await event.client.send_file(event.chat_id, f"port_{dosya}")
        os.remove(f"port_{dosya}")
        os.remove(f"{dosya}")
    elif re.search(borg3, dosy):
        await event.edit(LANG["UNIBORG3"])
        komu = re.findall(borg3, dosy)

        if len(komu) > 1:
            await event.edit(LANG["TOO_MANY_PLUGIN"])
            return

        komut = komu[0][1]

        degistir = dosy.replace('@borg.on(admin_cmd("' + komut + '"))', '@register(outgoing=True, pattern="^.' + komut + '")')
        degistir = degistir.replace("from userbot.utils import admin_cmd", "from userbot.events import register")
        degistir = re.sub(r"(from uniborg).*", "from userbot.events import register", degistir)
        degistir = degistir.replace("def _(event):", "def port_" + komut.replace("?(.*)", "") + "(event):")
        degistir = degistir.replace("borg.", "event.client.")

        ported = open(f'port_{dosya}', "w").write(degistir)

        await event.edit(LANG["UPLOADING"])

        await event.client.send_file(event.chat_id, f"port_{dosya}")
        os.remove(f"port_{dosya}")
        os.remove(f"{dosya}")

    else:
        await event.edit(LANG["UNIBORG_NOT_FOUND"])

@register(outgoing=True, pattern="^.plist")
async def plist(event):
    if PLUGIN_CHANNEL_ID != None:
        await event.edit(LANG["PLIST_CHECKING"])
        yuklenen = f"{LANG['PLIST']}\n\n"
        async for plugin in event.client.iter_messages(PLUGIN_CHANNEL_ID, filter=InputMessagesFilterDocument):
            try:
                dosyaismi = plugin.file.name.split(".")[1]
            except:
                continue

            if dosyaismi == "py":
                yuklenen += f"✨ {plugin.file.name}\n"
        await event.edit(yuklenen)
    else:
        await event.edit(LANG["TEMP_PLUGIN"])

@register(outgoing=True, pattern="^.pinstall")
async def pinstall(event):
    if event.is_reply:
        plugin = await event.get_reply_message()
    else:
        await event.edit(LANG["REPLY_TO_FILE"])
        return
    if event.is_reply:
        plugin = await event.get_reply_message()
        if not plugin.media or not plugin.file:
            await event.edit(LANG["PY_FAYL_CAVAB"])
            return
        if not plugin.file.name.endswith(".py"):
            await event.edit(LANG["PY_DEYIL"])
            return
    else:
        await event.edit(LANG["PY_FAYL_CAVAB"])
        return
    await event.edit(LANG["DOWNLOADING"])

    list = f'./userbot/modules/{plugin.file.name}'
    if exists(list):
        await event.edit("`Bu plugin onsuzda yüklənib. Onu ikinci dəfə yükləməyəcəm😌`")
        return
    fayl = await event.client.download_media(plugin, "./userbot/modules/")
   
    try:
        spec = importlib.util.spec_from_file_location(fayl, fayl)
        mod = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(mod)
    except Exception as e:
        await event.edit(f"{LANG['PLUGIN_BUGGED']} {e}`")
        return os.remove("./userbot/modules/" + fayl)

    dosy = open(fayl, "r").read()
    for T in TEHLUKELI:
      if re.search(T, dosy):
         os.remove(fayl)
         return await event.edit(f"**Yüklənmə dayandırıldı!**\n{plugin.file.name} faylında {T} tapıldı. Bu zərərli bir plugindir!\n\nƏgər siz bunun güvənli olduğunu düşünür və ya plugini özünüz üçün yaratmısınızsa bunu @LunaDestek adminlərinə bildirin")
    if re.search(r"@tgbot\.on\(.*pattern=(r|)\".*\".*\)", dosy):
        komu = re.findall(r"\(.*pattern=(r|)\"(.*)\".*\)", dosy)
        komutlar = ""
        i = 0
        while i < len(komu):
            komut = komu[i][1]
            CMD_HELP["tgbot_" + komut] = f"{LANG['PLUGIN_DESC']} {komut}"
            komutlar += komut + " "
            i += 1
        await event.edit(LANG['PLUGIN_DOWNLOADED'] % komutlar)
    else:
        Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", dosy)

        if (not type(Pattern) == list) or (len(Pattern) < 1 or len(Pattern[0]) < 1):
            if re.search(r'CmdHelp\(.*\)', dosy):
                cmdhelp = re.findall(r"CmdHelp\([\"'](.*)[\"']\)", dosy)[0]
                await plugin.forward_to(PLUGIN_CHANNEL_ID)
                return await event.edit(f'__📥 Plugin uğurla yükləndi!__\n`ℹ️ Daha ətraflı məlumat almaq üçün` **.luna {cmdhelp}** `yazın.`')
            else:
                await plugin.forward_to(PLUGIN_CHANNEL_ID)
                userbot.cmdhelp.CmdHelp(fayl).add_warning('Əmrlər tapılmadı!').add()
                return await event.edit(LANG['PLUGIN_DESCLESS'])
        else:
            if re.search(r'CmdHelp\(.*\)', dosy):
                cmdhelp = re.findall(r"CmdHelp\([\"'](.*)[\"']\)", dosy)[0]
                await plugin.forward_to(PLUGIN_CHANNEL_ID)
                return await event.edit(f'__📥 Plugin uğurla yükləndi!__\n`ℹ️ Daha ətraflı məlumat almaq üçün` **.luna {cmdhelp}** `yazın.`')
            else:
                dosyaAdi = plugin.file.name.replace('.py', '')
                extractCommands(fayl)
                await plugin.forward_to(PLUGIN_CHANNEL_ID)
                return await event.edit(f'__📥 Plugin uğurla yükləndi!__\n`ℹ️ Daha ətraflı məlumat almaq üçün` **.luna {dosyaAdi}** `yazın.`')

@register(outgoing=True, pattern="^.premove ?(.*)")
async def premove(event):
    modul = event.pattern_match.group(1).lower()
    if len(modul) < 1:
        await event.edit(LANG['PREMOVE_GIVE_NAME'])
        return

    await event.edit(LANG['PREMOVE_DELETING'])
    i = 0
    a = 0
    async for message in event.client.iter_messages(PLUGIN_CHANNEL_ID, filter=InputMessagesFilterDocument, search=modul):
        await message.delete()
        try:
            os.remove(f"./userbot/modules/{message.file.name}")
        except FileNotFoundError:
            await event.reply(LANG['ALREADY_DELETED'])

        i += 1
        if i > 1:
            break

    if i == 0:
        await event.edit(LANG['NOT_FOUND_PLUGIN'])
    else:
        await event.edit(LANG['PLUG_DELETED'])

@register(outgoing=True, pattern="^.psend ?(.*)")
async def psend(event):
    modul = event.pattern_match.group(1)
    if len(modul) < 1:
        await event.edit(LANG['PREMOVE_GIVE_NAME'])
        return

    if os.path.isfile(f"./userbot/modules/{modul}.py"):
        await event.client.send_file(event.chat_id, f"./userbot/modules/{modul}.py", caption=LANG['DTO_PLUGIN_CAPTION'])
        await event.delete()
    else:
        await event.edit(LANG['NOT_FOUND_PLUGIN'])


@register(outgoing=True, pattern="^.ptest")
async def ptest(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
    else:
        await event.edit(LANG["REPLY_TO_FILE"])
        return

    await event.edit(LANG["DOWNLOADING"])
    if not os.path.exists('./userbot/temp_plugins/'):
        os.makedirs('./userbot/temp_plugins')
    dosya = await event.client.download_media(reply_message, "./userbot/temp_plugins/")
    
    try:
        spec = importlib.util.spec_from_file_location(dosya, dosya)
        mod = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(mod)
    except Exception as e:
        await event.edit(f"{LANG['PLUGIN_BUGGED']} {e}`")
        return os.remove("./userbot/temp_plugins/" + dosya)

    return await event.edit(f'__📥 Plugin uğurla yükləndi!__\n`ℹ️ Ama əmri tapa bilmədim bot yenidən başladıldıqda plugin silinəcək.`')
