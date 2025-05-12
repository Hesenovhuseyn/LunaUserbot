import time
import importlib
import asyncio
from importlib import import_module
from sqlite3 import connect
import os
import requests
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.channels import GetMessagesRequest
from . import BRAIN_CHECKER, BOT_TOKEN, CMD_HELP, LUNA_VERSION, PATTERNS
from .modules import ALL_MODULES
import userbot.modules.sql_helper.mesaj_sql as MSJ_SQL
import userbot.modules.sql_helper.galeri_sql as GALERI_SQL
from pySmartDL import SmartDL
from telethon.tl import functions
from random import choice
import chromedriver_autoinstaller
from . import LANGUAGE, LOGS, bot, PLUGIN_CHANNEL_ID
from json import loads, JSONDecodeError
import re
import userbot.cmdhelp
from userbot.modules.sql_helper.lunauserbot.assistantbot import lunaassistantbot, heroku_qurulum
StartTime = time.time()

DIZCILIK_STR = [
    "SStikeri fırladıram...",
    "Yaşaşın fırlatmaq...",
    "Bu stikeri öz paketimə dəvət edirəm...",
    "Bunu fırlatmalıyam...",
    "Gözəl stikerdi!\nTəcili fırlatmalıyam..",
    "Stikerini fırladıram!\nhahaha.",
    "Buna ba (☉｡☉)!→\nMən bunu fırladarkən...",
    "Stikerivi oğurladım...",
    "Stiker qəfəsə salınır...",
    "Lotu totu stikerivi oğurladı... ",
]

AFKSTR = [
    "İndi təcili işim var, daha sonra mesaj atsan olar? Onsuz yenidən gələcəm.",
    "Bu nömrəyə zəng çatmır. Telefon ya söndürülüb yada əhatə dairəsi xaricindədi. Zəhmət olmasa yenidən cəhd edin. \nbiiiiiiiiiiiiiiiiiiiiiiiiiiiiip!",
    "Bir neçə dəqiqə içində gələcəyəm. Ancaq gəlməsəm...\ndaha çox gözlə.",
    "İndi burada deyiləm, başqa yerdəyəm.",
    "İnsan sevdiyini itirən zaman\ncanı yanar yanar yanaaaarrrr\nBoy bağışla 😂 bilmirdim burda kimsə var\nSahibim daha sonra sizə yazacaq.",
    "Bəzən həyatdakı ən yaxşı şeylər gözləməyə dəyər…\nTez qayıdaram.",
    "Tez qayıdaram,\nama əyər geri qayıtmasam,\ndaha sonra qayıdaram.",
    "Hələdə anlamadınsa,\nburada deyiləm.",
    "Aləm qalxsa səni məni məndən alnağa hamıdan alıb götürrəm səni...\nSahibim burada deil ama qruza salacaq mahnılar oxuya bilərəm 😓🚬",
    "7 dəniz və 7 ölkədən uzaqdayam,\n7 su və 7 qitə,\n7 dağ və 7 təpə,\n7 ovala və 7 höyük,\n7 hovuz və 7 göl,\n7 bahar və 7 çay,\n7 şəhər və 7 məhəllə,\n7 blok və 7 ev...\n\nMesajların belə mənə çatmayacağı yer!",
    "İndi klaviaturadan uzaqdayam, ama ekranınızda yeterincə yüksək səslə qışqırığ atsanız, sizi eşidə bilərəm.",
    "Bu tərəfdən irəlləyirəm\n---->",
    "Bu tərəfdən irəlləyirəm\n<----",
    "Zəhmət olmasa mesaj buraxın və məni olduğumdan daha önəmli hiss etdirin.",
    "Sahibim burda deil, buna görə mənə yazmağı dayandır.",
    "Burda olsaydım,\nSənə harada olduğumu deyərdim.\n\nAma mən deiləm,\ngeri qayıtdığımda məndən soruş...",
    "Uzaqlardayam!\nNə vaxt qayıdaram bilmirəm !\nBəlkə bir neçə dəqiqə sonra!",
    "Sahibim indi məşğuldu. Adınızı, nömrənizi və adresinizi versəniz ona yönləndirərəm və beləliklə geri gəldiyi zaman, sizə cavab yazar",
    "Bağışlayın, sahibim burda deil.\nO gələnə qədər mənimlə danışa bilərsən.\nSahibim sizə sonra yazar.",
    "Dünən gecə yarə namə yazdım qalmışam əllərdə ayaqlarda denən heç halımı soruşmazmı? Qalmışam əllərdə ayaqlarda\nSahibim burda deil ama sənə mahnı oxuyajammmm",
    "Həyat qısa, dəyməz qıza...\nNətər zarafat elədim?",
    "İndi burada deiləm....\nama burda olsaydım...\n\nbu möhtəşəm olardı eləmi qadan alım ?",
]

UNAPPROVED_MSG = ("Hey salam! {mention}! Qorxma, Bu bir botdur.\n\n"
                  "Sahibim sənə PM atma icazəsi verməyib. "
                  "Xaiş sahibimin aktiv olmasını gözlə, o adətən PM'ləri təsdiqləyir.\n\n"
                  "Təşəkkürlər ❤️")

DB = connect("upbrain.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()
INVALID_PH = '\nXƏTA: GirilƏN telefon nömrəsi keçərsizdir' \
             '\n  Məlumat: ölkə kodunu işlədərə nömrəni yaz' \
             '\n       Telefon nömrənizi təkrar yoxlayın'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("upbrain").close()

def extractCommands(file):
    FileRead = open(file, 'r').read()
    
    if '/' in file:
        file = file.split('/')[-1]

    Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", FileRead)
    Komutlar = []

    if re.search(r'CmdHelp\(.*\)', FileRead):
        pass
    else:
        dosyaAdi = file.replace('.py', '')
        CmdHelp = userbot.cmdhelp.CmdHelp(dosyaAdi, False)

        # Emrler #
        for Command in Pattern:
            Command = Command[1]
            if Command == '' or len(Command) <= 1:
                continue
            Komut = re.findall("(^.*[a-zA-Z0-9şğüöçı]\w)", Command)
            if (len(Komut) >= 1) and (not Komut[0] == ''):
                Komut = Komut[0]
                if Komut[0] == '^':
                    KomutStr = Komut[1:]
                    if KomutStr[0] == '.':
                        KomutStr = KomutStr[1:]
                    Komutlar.append(KomutStr)
                else:
                    if Command[0] == '^':
                        KomutStr = Command[1:]
                        if KomutStr[0] == '.':
                            KomutStr = KomutStr[1:]
                        else:
                            KomutStr = Command
                        Komutlar.append(KomutStr)

            # DTOPY
            Dtopy = re.search('\"\"\"DTOPY(.*)\"\"\"', FileRead, re.DOTALL)
            if not Dtopy == None:
                Dtopy = Dtopy.group(0)
                for Satir in Dtopy.splitlines():
                    if (not '"""' in Satir) and (':' in Satir):
                        Satir = Satir.split(':')
                        Isim = Satir[0]
                        Deger = Satir[1][1:]
                                
                        if Isim == 'INFO':
                            CmdHelp.add_info(Deger)
                        elif Isim == 'WARN':
                            CmdHelp.add_warning(Deger)
                        else:
                            CmdHelp.set_file_info(Isim, Deger)
            for Komut in Komutlar:
                # if re.search('\[(\w*)\]', Komut):
                    # Komut = re.sub('(?<=\[.)[A-Za-z0-9_]*\]', '', Komut).replace('[', '')
                CmdHelp.add_command(Komut, None, 'Bu plugin qırağdan yüklənib. Hər hansısa bir açıqlama yazılmayıb.')
            CmdHelp.add()

try:
    bot.start()
    if not bot.is_connected:
        LOGS.error("Bot bağlantısı sağlanamadı. Çıkılıyor.")
        exit(1)

    idim = bot.get_me().id
    dtobl = requests.get('https://raw.githubusercontent.com/Hesenovhuseyn/LunaUserbot//master/upx.json').json()
    if idim in dtobl:
        LOGS.info("Kullanıcı botu kapatıyor.")
        bot.disconnect()

    # ChromeDriver #
    try:
        chromedriver_autoinstaller.install()
    except:
        pass

    # Galeri için değerler
    GALERI = {}

    # PLUGIN MESAJLARI AYARLIYORUZ
    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {"alive": "❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️ 𝓐𝓴𝓽𝓲𝓿𝓭𝓲𝓻...", 
                           "afk": f"{str(choice(AFKSTR))}", 
                           "kickme": "Bye-bye mən qrupdan çıxdım 🥰", 
                           "pm": UNAPPROVED_MSG, 
                           "dızcı": str(choice(DIZCILIK_STR)), 
                           "ban": "{mention}, banlandı!", 
                           "mute": "{mention}, susduruldu!", 
                           "approve": "{mention}, mənə mesaj göndərə bilərsən!", 
                           "disapprove": "{mention}, artıq mənə mesaj göndərə bilmərsən!", 
                           "block": "{mention}, bloklandın!", 
                           "restart": "❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️💻 𝚢𝚎𝚗𝚒𝚍ə𝚗 𝚋𝚊ş𝚕𝚊𝚍ı𝚕ı𝚛. . ."}

    PLUGIN_MESAJLAR_TURLER = ["alive", "afk", "kickme", "pm", "dızcı", "ban", "mute", "approve", "disapprove", "block", "restart"]
    for mesaj in PLUGIN_MESAJLAR_TURLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if dmsj == False:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            if dmsj.startswith("MEDYA_"):
                medya = int(dmsj.split("MEDYA_")[1])
                medya = bot.get_messages(PLUGIN_CHANNEL_ID, ids=medya)
                PLUGIN_MESAJLAR[mesaj] = medya
            else:
                PLUGIN_MESAJLAR[mesaj] = dmsj
    
    
    zararli_deyisenler = ["off_repo", "Repo", "git", "GitCommandError"]

    def zararli_kod_varmi(file_content):
        for var in zararli_deyisenler:
            if var in file_content:
                return True
        return False

    if PLUGIN_CHANNEL_ID is not None:
        LOGS.info("Pluginlər Yüklənir")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
        except:
            KanalId = "me"

        try:
            for plugin in bot.iter_messages(KanalId, filter=InputMessagesFilterDocument):
                if plugin.file.name and (len(plugin.file.name.split('.')) > 1) and plugin.file.name.split('.')[-1] == 'py':
                    Split = plugin.file.name.split('.')

                    if not os.path.exists("./userbot/modules/" + plugin.file.name):
                        dosya = bot.download_media(plugin, "./userbot/modules/")
                    else:
                        LOGS.info("Bu Plugin Onsuz Yüklənib " + plugin.file.name)
                        extractCommands('./userbot/modules/' + plugin.file.name)
                        dosya = plugin.file.name
                        continue
                
            
                    with open("./userbot/modules/" + plugin.file.name, 'r') as f:
                        file_content = f.read()

                
                    if zararli_kod_varmi(file_content):
                        LOGS.info(f"Plugin '{plugin.file.name}' yüklənmədi ")
                        continue

                    try:
                        spec = importlib.util.spec_from_file_location("userbot.modules." + Split[0], dosya)
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)
                    except Exception as e:
                        LOGS.info(f"Yükləmə uğursuz! Plugin xətalıdır.\n\nXəta: {e}")
                        try:
                            plugin.delete()
                        except:
                            pass
                        if os.path.exists("./userbot/modules/" + plugin.file.name):
                            os.remove("./userbot/modules/" + plugin.file.name)
                        continue
                    extractCommands('./userbot/modules/' + plugin.file.name)
        except ConnectionError as e:
            LOGS.error(f"Bağlantı hatası: {e}")
    else:
        bot.send_message("me", "Xahiş, pluginlərin qalıcı olması üçün PLUGIN_CHANNEL_ID-i düzəldin.")
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

async def FotoDegistir (foto):
    FOTOURL = GALERI_SQL.TUM_GALERI[foto].foto
    r = requests.get(FOTOURL)

    with open(str(foto) + ".jpg", 'wb') as f:
        f.write(r.content)    
    file = await bot.upload_file(str(foto) + ".jpg")
    try:
        await bot(functions.photos.UploadProfilePhotoRequest(
            file
        ))
        return True
    except:
        return False

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("Botunuz işleyir! Her hansi bir söhbete .alive yazaraq Test edin."
          " Yardıma ehtiyacınız varsa, Destek qrupumuza buyurun t.me/silgiub")
LOGS.info(f"Bot versiyası:❤️𝑳𝒖𝒏𝒂𝑼𝒔𝒆𝒓𝒃𝒐𝒕❤️ {LUNA_VERSION}")

"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""


app, config = heroku_qurulum()

if config:
    if "BOT_TOKEN" not in config:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(lunaassistantbot(app, config))


bot.run_until_disconnected()
