import os
from telethon.tl.types import ChatBannedRights
from pymongo import MongoClient


class Config(object):
    LOGGER = True
    APP_ID = int(os.environ.get("APP_ID", 6))
    API_HASH = os.environ.get("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
    SCREEN_SHOT_LAYER_ACCESS_KEY = os.environ.get(
        "SCREEN_SHOT_LAYER_ACCESS_KEY", None)
    OPEN_WEATHER_MAP_APPID = os.environ.get("OPEN_WEATHER_MAP_APPID", None)
    PRIVATE_GROUP_BOT_API_ID = os.environ.get("PRIVATE_GROUP_BOT_API_ID", None)
    if PRIVATE_GROUP_BOT_API_ID:
        PRIVATE_GROUP_BOT_API_ID = int(PRIVATE_GROUP_BOT_API_ID)
    PRIVATE_CHANNEL_BOT_API_ID = os.environ.get(
        "PRIVATE_CHANNEL_BOT_API_ID", None)
    if PRIVATE_CHANNEL_BOT_API_ID:
        PRIVATE_CHANNEL_BOT_API_ID = int(PRIVATE_CHANNEL_BOT_API_ID)
    TMP_DOWNLOAD_DIRECTORY = os.environ.get(
        "TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")

    IBM_WATSON_CRED_URL = os.environ.get("IBM_WATSON_CRED_URL", None)
    IBM_WATSON_CRED_PASSWORD = os.environ.get("IBM_WATSON_CRED_PASSWORD", None)
    TELEGRAPH_SHORT_NAME = os.environ.get("TELEGRAPH_SHORT_NAME", "mrconfused")
    GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN", None)
    GIT_REPO_NAME = os.environ.get("GIT_REPO_NAME", None)
    OCR_SPACE_API_KEY = os.environ.get("OCR_SPACE_API_KEY", None)
    
    TG_GLOBAL_ALBUM_LIMIT = int(os.environ.get("TG_GLOBAL_ALBUM_LIMIT", 9))
    # @BotFather'dan BOT Token Telegram
    TG_BOT_TOKEN_BF_HER = os.environ.get("TG_BOT_TOKEN_BF_HER", None)
    TG_BOT_USER_NAME_BF_HER = os.environ.get("TG_BOT_USER_NAME_BF_HER", None)
    NO_LOG_P_M_S = bool(os.environ.get("NO_LOG_P_M_S", True))
    THUMB_IMAGE = os.environ.get(
        "THUMB_IMAGE",
        "https://files.catbox.moe/unuq2j.jpg")
    GENIUS_API_TOKEN = os.environ.get("GENIUS_API_TOKEN", None)
    MAX_MESSAGE_SIZE_LIMIT = 4095
    UB_BLACK_LIST_CHAT = set(
        int(x) for x in os.environ.get(
            "UB_BLACK_LIST_CHAT", "").split())
    LOAD = []
    MAX_ANTI_FLOOD_MESSAGES = 10
    ANTI_FLOOD_WARN_MODE = ChatBannedRights(
        until_date=None,
        view_messages=None,
        send_messages=True
    )
    CHATS_TO_MONITOR_FOR_ANTI_FLOOD = []
    NO_LOAD = [
        "notification_mtab_manager",
        "dbhelper",
        "fban_gban",
        "unbanmute",
    ]
    ALIVE_PIC = os.environ.get("ALIVE_PIC", None)
    PMPERMIT_PIC = os.environ.get("PMPERMIT_PIC", None)
    CUSTOM_PMPERMIT_TEXT = os.environ.get("CUSTOM_PMPERMIT_TEXT", None)
    REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)
    SLAP_USERNAME = os.environ.get("SLAP_USERNAME", None)
    DB_URI = os.environ.get("DATABASE_URL", None)
    NO_OF_BUTTONS_DISPLAYED_IN_H_ME_CMD = int(
        os.environ.get("NO_OF_BUTTONS_DISPLAYED_IN_H_ME_CMD", 7))
    NO_OF_COLOUMS_DISPLAYED_IN_H_ME_CMD = int(
        os.environ.get("NO_OF_COLOUMS_DISPLAYED_IN_H_ME_CMD", 3))
    EMOJI_TO_DISPLAY_IN_HELP = os.environ.get("EMOJI_TO_DISPLAY_IN_HELP", " ")
    COMMAND_HAND_LER = os.environ.get("COMMAND_HAND_LER", r"\.")
    SUDO_COMMAND_HAND_LER = os.environ.get("SUDO_COMMAND_HAND_LER", r"\.")
    HELP_INLINETYPE = os.environ.get("HELP_INLINETYPE", None)
    SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
    VERY_STREAM_LOGIN = os.environ.get("VERY_STREAM_LOGIN", None)
    VERY_STREAM_KEY = os.environ.get("VERY_STREAM_KEY", None)
    CHROME_BIN = os.environ.get("CHROME_BIN", "/usr/bin/google-chrome")
    CHROME_DRIVER = os.environ.get("CHROME_DRIVER", "/usr/bin/chromedriver")
    G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID", None)
    G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET", None)
    G_DRIVE_AUTH_TOKEN_DATA = os.environ.get("G_DRIVE_AUTH_TOKEN_DATA", None)
    #  AUTH_TOKEN_DATA = os.environ.get("AUTH_TOKEN_DATA", None)
    # os.makedirs(TMP_DOWNLOAD_DIRECTORY, exist_ok=True)
    # t_file = open(TMP_DOWNLOAD_DIRECTORY+"auth_token.txt","w")
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    TELE_GRAM_2FA_CODE = os.environ.get("TELE_GRAM_2FA_CODE", None)
    GROUP_REG_SED_EX_BOT_S = os.environ.get(
        "GROUP_REG_SED_EX_BOT_S",
        r"(regex|moku|BananaButler_|rgx|l4mR)bot")
    # rapidleech plugins
    DOWNLOAD_PFP_URL_CLOCK = os.environ.get("DOWNLOAD_PFP_URL_CLOCK", None)
    # Google Chrome Selenium Stuff
    # taken from
    # https://github.com/jaskaranSM/UniBorg/blob/9072e3580cc6c98d46f30e41edbe73ffc9d850d3/sample_config.py#L104-L106
    TEMP_DIR = os.environ.get("TEMP_DIR", "./DOWNLOADS")
    # spotify stuff
    DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)
    SPOTIFY_BIO_PREFIX = os.environ.get("SPOTIFY_BIO_PREFIX", None)
    SPOTIFY_PASS = os.environ.get("SPOTIFY_PASS", None)
    SPOTIFY_USERNAME = os.environ.get("SPOTIFY_USERNAME", None)
    GDRIVE_FOLDER_ID = os.environ.get("GDRIVE_FOLDER_ID", None)
    LYDIA_API = os.environ.get("LYDIA_API", None)
    DEFAULT_NAME = os.environ.get("DEFAULT_NAME", None)
    VIRUSTOTAL_API_KEY = os.environ.get("VIRUSTOTAL_API_KEY", None)
    MAX_FLOOD_IN_P_M_s = int(os.environ.get("MAX_FLOOD_IN_P_M_s", 5))
    PM_LOGGR_BOT_API_ID = os.environ.get("PM_LOGGR_BOT_API_ID", None)
    if PM_LOGGR_BOT_API_ID:
        PM_LOGGR_BOT_API_ID = int(PM_LOGGR_BOT_API_ID)
    DUAL_LOG = os.environ.get("DUAL_LOG", False)
    TL_VID_STREAM_TYPES = ("MKV", "MP4", "WEBM")
    TL_MUS_STREAM_TYPES = ("MP3", "WAV", "FLAC")
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)
    # MONGOCLIENT = pymongo.MongoClient(MONGO_DB_URI)
    # MONGO = MONGOCLIENT.userbot
    # JustWatch Country
    WATCH_COUNTRY = os.environ.get("WATCH_COUNTRY", "IN")
    TZ = os.environ.get("TZ", None)
    # RSS_POST_MSG_GROUP_ID = map(int, os.environ.get("RSS_POST_MSG_GROUP_ID", None).split())
    RSS_POST_MSG_GROUP_ID = os.environ.get("RSS_POST_MSG_GROUP_ID", None)
    if RSS_POST_MSG_GROUP_ID:
        RSS_POST_MSG_GROUP_ID = int(RSS_POST_MSG_GROUP_ID)
    SPAM_WATCH_API = os.environ.get("SPAM_WATCH_API", None)


class Production(Config):
    LOGGER = False
 

class Development(Config):
    LOGGER = True


# Init Mongo
MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
MONGOCLIENT = MongoClient(MONGO_DB_URI, 27017, serverSelectionTimeoutMS=1)
MONGO = MONGOCLIENT.userbot


def is_mongo_alive():
    try:
        MONGOCLIENT.server_info()
    except BaseException as e:
        print(e)
        return Fa
