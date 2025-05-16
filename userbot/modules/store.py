
import os
from telethon.tl.types import InputMessagesFilterDocument
from userbot.events import register
from userbot import BOT_USERNAME, PATTERNS, CMD_HELP, PLUGIN_CHANNEL_ID
import userbot.cmdhelp
from random import choice, sample
import importlib
import re

# ██████ LANGUAGE CONSTANTS ██████ #

from userbot.language import get_value
LANG = get_value("__plugin")

# ████████████████████████████████ #

# Plugin Maqazini
@register(outgoing=True, pattern="^.store ?(.*)")
@register(outgoing=True, pattern="^.ma[gğ]aza ?(.*)")
async def magaza(event):
    plugin = event.pattern_match.group(1)
    await event.edit('**[❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️](@LunaDestek) Plugin Mağazası**\n__Versiya 2.3__\n\n`🔎 Plugin\'i axtarıram... Xaiş biraz gözlə.`')
    split = plugin.split()
    if plugin == '':
        plugin = 'Son yüklənən'
        plugins = await event.client.get_messages('@silgiubplugin', limit=15, filter=InputMessagesFilterDocument)
    elif len(split) >= 1 and (split[0] == 'random' or split[0] == 'rastgele'):
        plugin = 'Təsadufi'
        plugins = await event.client.get_messages('@LunaPlugins', limit=None, filter=InputMessagesFilterDocument)
        plugins = sample(plugins, int(split[1]) if len(split) == 2 else 5)
    else:
        plugins = await event.client.get_messages('@LunaPlugins', limit=None, search=plugin, filter=InputMessagesFilterDocument)
        random = await event.client.get_messages('@LunaPlugins', limit=None, filter=InputMessagesFilterDocument)
        random = choice(random)
        random_file = random.file.name

    result = f'**[❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️](@LunaDestek) Plugin Mağazası**\n\n**🔎 Axtarış:** `{plugin}`\n**🔢 Nəticələr: __({len(plugins)})__**\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n'
    
    if len(plugins) == 0:
        result += f'**Həç bir şey tapa bilmədim...**\n`{random_file}` __plugininə nə deirsən?__'
    else:
        for plugin in plugins:
            plugin_lines = plugin.raw_text.splitlines()
            if len(plugin_lines) > 0:  # Check if there are any lines
                result += f'⬇️ {plugin_lines[0]} ({plugin.file.name}): '
                if len(plugin_lines[2]) < 50:
                    result += f'{plugin_lines[2]}'
                else:
                    result += f'{plugin_lines[2][:50]}...'
                result += f'\nℹ️ Yükləmək üçün: {PATTERNS[:1]}sinstall {plugin.id}\n➖➖➖➖➖\n'
            else:
                result += f'⚠️ Plugin mətnində səhv var və ya plugin boşdur. `{plugin.file.name}`\n'
                
    return await event.edit(result)

# Plugin Mağazası
@register(outgoing=True, pattern="^.sy[üu]kle ?(.*)")
@register(outgoing=True, pattern="^.sinstall ?(.*)")
async def sinstall(event):
    plugin = event.pattern_match.group(1)
    try:
        plugin = int(plugin)
    except:
        return await event.edit('**[❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️](@LunaDestek) Plugin Mağazası**\n__Versiya 2.3__\n\n**⚠️ Xəta:** `Xaiş sadəcə rəqəm yazın. Əgəe Plugin axtarmaq istəyirsizsə .store əmrini işlədin.`')
    
    await event.edit('**[❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️](@LunaDestek) Plugin Mağazası**\n\n`🔎 Plugin\'i gətirirəm... Xaiş biraz gözlə.`')
    plugin = await event.client.get_messages('@silgiubplugin', ids=plugin)
    await event.edit(f'**[❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️](@LunaDestek) Plugin Mağazası**\n\n`✅ {plugin.file.name} plugini gətirildi!`\n`⬇️ Plugini yükləyirəm... Xaiş gözləyin.`')
    dosya = await plugin.download_media('./userbot/modules/')
    await event.edit(f'**[❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️](@LunaDestek) Plugin Mağazası**\n\n`✅ {plugin.file.name} yüklənmə uğurlu oldu!`\n`⬇️ Plugini yükləyirəm... Xaiş gözləyin.`')
    
    try:
        spec = importlib.util.spec_from_file_location(dosya, dosya)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as e:
        os.remove("./userbot/modules/" + dosya)
        return await event.edit(f'**[❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️](@LunaDestek) Plugin Mağazası**\n\n**⚠️ Xəta:** `Plugin xətalıdır. {e}`\n**XAİŞ BUNU İDARƏÇİLƏRƏ BİLDİRİN!**')

    dosy = open(dosya, "r").read()
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
        Komutlar = []

        if (not type(Pattern) == list) or (len(Pattern) < 1 or len(Pattern[0]) < 1):
            CMD_HELP[dosya] = LANG['PLUGIN_WITHOUT_DESC']
            return await event.edit(LANG['PLUGIN_DESCLESS'])
        else:
            if re.search(r'CmdHelp\(.*\)', dosy):
                cmdhelp = re.findall(r"CmdHelp\([\"'](.*)[\"']\)", dosy)[0]
                await plugin.forward_to(PLUGIN_CHANNEL_ID)
                return await event.edit(f'**[❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️](@LunaDestek) Plugin Mağazası**\n\n**✅ Modul uğurlar yükləndi!**\n__ℹ️ Modulun əmrləri və işlədilişi haqqında məlumat almaq üçün__ `.silgi {cmdhelp}` __yazın.__')
            else:
                dosyaAdi = plugin.file.name.replace('.py', '')
                CmdHelp = userbot.cmdhelp.CmdHelp(dosyaAdi, False)
                #  #
                for Command in Pattern:
                    Command = Command[1]
                    if Command == '' or len(Command) <= 1:
                        continue
                    Komut = re.findall("([^.].*\w)(\W*)", Command)
                    if (len(Komut[0]) > 1) and (not Komut[0][1] == ''):
                        KomutStr = Command.replace(Komut[0][1], '')
                        if KomutStr[0] == '^':
                            KomutStr = KomutStr[1:]
                            if KomutStr[0] == '.':
                                KomutStr = PATTERNS[:1] + KomutStr[1:]
                        Komutlar.append(KomutStr)
                    else:
                        if Command[0] == '^':
                            KomutStr = Command[1:]
                            if KomutStr[0] == '.':
                                KomutStr = PATTERNS[:1] + KomutStr[1:]
                        else:
                            KomutStr = Command
                        Komutlar.append(KomutStr)

                # DtoPY
                Dtopy = re.search('\"\"\"DTOPY(.*)\"\"\"', dosy, re.DOTALL)
                if not Dtopy == None:
                    Dtopy = Dtopy.group(0)
                    for Satir in Dtopy.splitlines():
                        if (not '"""' in Satir) and (':' in Satir):
                            Satir = Satir.split(':')
                            Isim = Satir[0]
                            Deger = Satir[1][1:]

                            CmdHelp.set_file_info(Isim, Deger)
                            
                for Komut in Komutlar:
                    CmdHelp.add_command(Komut, None, 'Bu plugin qırağdan yüklənib. Hər hansı bir açıqlama edilməyib.')
                CmdHelp.add()
                await plugin.forward_to(PLUGIN_CHANNEL_ID)
                return await event.edit(f'**[❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️](@LunaDestek) Plugin Mağazası**\n\n**✅ Modül uğurla yükləndi!**\n__ℹ️ Modulun əmrləri və işlədilişi haqqında məlumat almaq üçün` `.silgi {dosyaAdi}` `yazın.__')

userbot.cmdhelp.CmdHelp('store').add_command(
    'store', '<söz>', 'Plugin kanalına son atılan Pluginləri gətirər. Əgər söz yazarsanız axtarış edər.'
).add_command(
    'store random', '<rəqəm>', 'Plugin kanalından təsadufi plugin gətirər.', 'store random 10'
).add_command(
    'sinstall', '<rəqəm>', 'Plugin kanalından tez olaraq Plugini yükləyər.'
).add()
