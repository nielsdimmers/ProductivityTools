# daily.py
import requests
import notionInterface
import urllib.parse
import config

config = config.config()

notion = notionInterface.notion(config)

result = notion.getDailyData()

# the telegram URL to send a message to myself
telegramURL = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s" % (config.getItem('telegram','TELEGRAM_API_TOKEN'),config.getItem('telegram','TELEGRAM_CHAT_ID'),urllib.parse.quote(result))

# Send the message, print the result.
print(str(requests.get(telegramURL)))