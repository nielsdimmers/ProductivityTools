# daily.py
import configparser
import requests
import notionInterface
import sys

if len(sys.argv) >= 3 and sys.argv[1]=='--config':
	configFile = sys.argv[2]
else:
	configFile = 'config'

# Parse the notion vars from the config file
configParser = configparser.RawConfigParser()
configParser.read(configFile)

notion = notionInterface.notion(configParser)

result = notion.getDailyData()

# the telegram URL to send a message to myself
telegramURL = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=" % (configParser.get('telegram','TELEGRAM_API_TOKEN'),configParser.get('telegram','TELEGRAM_CHAT_ID'))

# Send the message, print the result.
print(str(requests.get(telegramURL+result)))













