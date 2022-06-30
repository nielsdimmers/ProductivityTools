# daily.py
import configparser
import sys
import requests
import datetime

if len(sys.argv) >= 3 and sys.argv[1]=='--config':
	configFile = sys.argv[2]
else:
	configFile = 'config'

# Parse the notion vars from the config file
configParser = configparser.RawConfigParser()
configParser.read(configFile)

# Parse the authentication
auth = 'Bearer %s' % configParser.get('notion','ACCESS_KEY')

# JSON Headers for the notion call
headers = {'Authorization': auth, 'Content-Type':'application/json','Notion-Version':'2022-02-22'}

# Url for the notion call
request_URL = 'https://api.notion.com/v1/databases/%s/query' % configParser.get('notion','TASK_DATABASE_KEY')

 # Today's date formatted in a way notion likes it, for the payload json
today = datetime.datetime.now().strftime("%Y-%m-%d")

# Payload json to filter out done, dropped and not yet due tasks
payload = {"filter": {
	"and": [
		{
			"property": "Status",
			"select" : {
				"does_not_equal": "Done 🙌"
			}
		}, 
		{
			"property": "Status",
      "select" : {
      	"does_not_equal": "Dropped 🔥"
      }
    },
    {
   "or": [
				{
					"property":"Due date",
					"date" :{
						"on_or_before":today
					}
				},
				{
					"property":"Action date",
					"date" : {
						"on_or_before":today
					}
				}
			]
    }
  ]
}
}

# Get the notion stuff
response = requests.post(request_URL, json=payload,headers=headers)

result = ""

result += "Good morning Niels, for today, there are a total of %s tasks:\n" % len(response.json()['results'])

# Generate a list of tasks
for task in response.json()['results']:
	status = task['properties']['Status']['select']
	if str(type(status)) == '<class \'NoneType\'>':
		status = 'no status selected!'
	else:
		status = status['name']
	
	result += "- %s (%s) \n" % (task['properties']['Name']['title'][0]['plain_text'],status)

#print()

# the telegram URL to send a message to myself
telegramURL = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=" % (configParser.get('telegram','TELEGRAM_API_TOKEN'),configParser.get('telegram','TELEGRAM_CHAT_ID'))

# Send the message, print the result.
print(str(requests.get(telegramURL+result)))













