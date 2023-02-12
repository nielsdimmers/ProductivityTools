from Nconfig import config
import requests
import urllib.parse
from global_vars import global_vars
import log

log = log.log()
config = config.config()

response = requests.get(global_vars.TELEGRAM_MSG_URL % (config.get_item('telegram','TELEGRAM_API_TOKEN'),config.get_item('telegram','TELEGRAM_CHAT_ID'),urllib.parse.quote(log.get_size_message())))