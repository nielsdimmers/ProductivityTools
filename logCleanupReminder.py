import config
import requests
import urllib.parse

config = config.config()

numLines = sum(1 for line in open(config.getItem('general','LOGFILE_NAME')))

message = 'The logfile %s is %s lines long.' % (config.getItem('general','LOGFILE_NAME'), numLines)

# the telegram URL to send a message to myself
telegramURL = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s" % (config.getItem('telegram','TELEGRAM_API_TOKEN'),config.getItem('telegram','TELEGRAM_CHAT_ID'),urllib.parse.quote(message))

response = requests.get(telegramURL)