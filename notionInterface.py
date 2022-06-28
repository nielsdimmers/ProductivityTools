import configparser
import requests
import datetime

# Notion interface to interact with notion
class notion:

	# Initialise config parser, given from source	
	def __init__(self, config):
		global configParser
		configParser = config

	# Returns the headers of the notion message
	def getNotionHeaders(self):
		return {'Authorization': 'Bearer %s' % configParser.get('notion','ACCESS_KEY'), 'Content-Type':'application/json','Notion-Version':'2022-02-22'}
	
	# Returns the JSON part of the groceries page
	def getGroceries(self):
		response = requests.get('https://api.notion.com/v1/blocks/%s/children' % configParser.get('notion','GROCERIES_PAGE_KEY') ,headers=self.getNotionHeaders())
		return response.json()
	
	# create a task object based on the given title
	# Returns a string representation of what happened (succesful, error, what kind of error...)
	def createTask(self,taskTitle):
		# JSON body
		dictionary = {'parent':{'database_id':configParser.get('notion','INBOX_DATABASE_KEY')}, 'properties':{'title':{'title':[{"text":{"content":taskTitle}}]}}}

		# The creation of the task
		response = requests.post('https://api.notion.com/v1/pages', json=dictionary,headers=self.getNotionHeaders())
		
		# Setup the response telegram message
		return "Created task with id [%s](%s). Status code: %s (%s)" % (response.json()['id'],response.json()['url'],response.status_code,response.reason)

	# add a grocery to the grocery pae
	def addGrocery(self,grocery):
		newGrocery = {'children':[{'object':'block', 'type':'to_do', 'to_do':{'rich_text':[{'type':'text','text': {'content': grocery} }] }}]}
		appendResponse = requests.patch('https://api.notion.com/v1/blocks/%s/children' % configParser.get('notion','GROCERIES_PAGE_KEY'),json=newGrocery,headers=self.getNotionHeaders())
		return 'Added grocery: %s' % grocery
		
	def getDailyData(self):
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
		response = requests.post(request_URL, json=payload,headers=self.getNotionHeaders())

		result = ""

		result += "Good morning Niels, for today, there are a total of %s tasks:\n" % len(response.json()['results'])

		# Generate a list of tasks
		for task in response.json()['results']:
			result += "- %s (%s) \n" % (task['properties']['Name']['title'][0]['plain_text'],task['properties']['Status']['select']['name'])
		
		return result
