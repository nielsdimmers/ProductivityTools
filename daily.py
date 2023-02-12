# daily.py
import requests
import notion_interface
import urllib.parse
from Nconfig import config
from global_vars import global_vars

config = config.config()
notion = notion_interface.notion()
result = notion.get_daily_data()

requests.get(global_vars.TELEGRAM_MSG_URL % (config.get_item('telegram','TELEGRAM_API_TOKEN'),config.get_item('telegram','TELEGRAM_CHAT_ID'),urllib.parse.quote(result)))