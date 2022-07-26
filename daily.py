# daily.py
import requests
import notion_interface
import urllib.parse
import config

config = config.config()

notion = notion_interface.notion(config)

result = notion.get_daily_data()

# the telegram URL to send a message to myself
telegramURL = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s" % (config.get_item('telegram','TELEGRAM_API_TOKEN'),config.get_item('telegram','TELEGRAM_CHAT_ID'),urllib.parse.quote(result))

# Send the message, print the result.
print(str(requests.get(telegramURL)))