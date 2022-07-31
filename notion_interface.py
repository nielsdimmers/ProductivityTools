import configparser
import requests
import datetime

# Notion interface to interact with notion
class notion:

	# Initialise config parser, given from source	
	def __init__(self, _config_parser):
		global config
		config = _config_parser

	# Returns the headers of the notion message
	def get_notion_headers(self):
		return {'Authorization': 'Bearer %s' % config.get_item('notion','ACCESS_KEY'), 'Content-Type':'application/json','Notion-Version':'2022-02-22'}
	
	# Returns the JSON part of the groceries page
	def get_groceries(self):
		response = requests.get('https://api.notion.com/v1/blocks/%s/children' % config.get_item('notion','GROCERIES_PAGE_KEY') ,headers=self.get_notion_headers())
		return response.json()
	
	# create a task object based on the given title
	# Returns a string representation of what happened (succesful, error, what kind of error...)
	def create_task(self,_task_title):
		# JSON body
		dictionary = {'parent':{'database_id':config.get_item('notion','INBOX_DATABASE_KEY')}, 'properties':{'title':{'title':[{"text":{"content":_task_title}}]}}}

		# The creation of the task
		response = requests.post('https://api.notion.com/v1/pages', json=dictionary,headers=self.get_notion_headers())
		
		# Setup the response telegram message
		return "Created task with id [%s](%s). Status code: %s (%s)" % (response.json()['id'],response.json()['url'],response.status_code,response.reason)

	# add a grocery to the grocery list
	def add_grocery(self,_grocery):
		new_grocery = {'children':[{'object':'block', 'type':'to_do', 'to_do':{'rich_text':[{'type':'text','text': {'content': _grocery} }] }}]}
		requests.patch('https://api.notion.com/v1/blocks/%s/children' % config.get_item('notion','GROCERIES_PAGE_KEY'),json=new_grocery,headers=self.get_notion_headers())
		return 'Added grocery: %s' % _grocery
		
	def get_groceries_url(self):
		return config.get_item('notion','GROCERIES_PAGE_URL')
		
	def get_daily_data(self):
		# Url for the notion call
		request_url = 'https://api.notion.com/v1/databases/%s/query' % config.get_item('notion','TASK_DATABASE_KEY')

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
		response = requests.post(request_url, json=payload,headers=self.get_notion_headers())
		
		result = ""
		result += "Good morning Niels, for today, there are a total of %s tasks:\n" % len(response.json()['results'])
		
		# Generate a list of tasks
		for task in response.json()['results']:
			result += "- %s (%s) \n" % (task['properties']['Name']['title'][0]['plain_text'],task['properties']['Status']['select']['name'])
		
		## *** Journal goal retrieving ***
		
		payload = {"filter": {
			"or" : [
			{
				"property" : "title",
				"title" : {
					"starts_with" : today
				}
			},
			{
				"property" : "Date",
				"date" : {
					"equals" : today
				}
			}
			]
		}
		}
		
		request_url = 'https://api.notion.com/v1/databases/%s/query' % config.get_item('notion','INBOX_JOURNAL_KEY')
		
		response = requests.post(request_url, json = payload,headers=self.get_notion_headers())
		
		if len(response.json()['results']) > 0 and len(response.json()['results'][0]['properties']['Doel (Commander\'s Intent)']['rich_text']) > 0:
			result += '\n\nThe goal for today (Commander\'s Intent): %s' % response.json()['results'][0]['properties']['Doel (Commander\'s Intent)']['rich_text'][0]['plain_text']
		else:
			result += '\n\nThere is no goal defined for today'
		
		return result
