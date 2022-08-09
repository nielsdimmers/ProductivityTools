# daily.py
import requests
import notion_interface
import urllib.parse
import config

telegram_config = config.config()

notion = notion_interface.notion()

result = notion.get_daily_data()

# the telegram URL to send a message to myself
telegramURL = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s" % (telegram_config.get_item('telegram','TELEGRAM_API_TOKEN'),telegram_config.get_item('telegram','TELEGRAM_CHAT_ID'),urllib.parse.quote(result))

requests.get(telegramURL)