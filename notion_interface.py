import configparser
import requests
import datetime
from global_vars import global_vars
from notion_journal_interface import notion_journal
import config

# Notion interface to interact with notion
class notion:

	config = config.config('config_notion')

	# Returns the headers of the notion message
	def get_notion_headers(self):
		return {'Authorization': 'Bearer %s' % self.config.get_item('notion','ACCESS_KEY'), 'Content-Type':'application/json','Notion-Version':'2022-02-22'}
	
	# Returns the JSON part of the groceries page
	def get_groceries(self):
		response = requests.get(global_vars.NOTION_CHILDREN_URL % self.config.get_item('notion','GROCERIES_PAGE_KEY') ,headers=self.get_notion_headers())
		return response.json()
	
	# create a task object based on the given title
	# Returns a string representation of what happened (succesful, error, what kind of error...)
	def create_task(self,_task_data):
		
		task_data = _task_data.split('\n') # Split the task data by the delimiter defining between title [0] and the contents [1..*]
		
		# JSON body
		dictionary = {'parent':{'database_id':self.config.get_item('notion','INBOX_DATABASE_KEY')}, 'properties':{'title':{'title':[{"text":{"content":task_data[0]}}]}}}

		# The creation of the task
		response = requests.post('https://api.notion.com/v1/pages', json=dictionary,headers=self.get_notion_headers())
		
		task_data.pop(0) ## remove the title from the array
		
		for content in task_data:
			task_content = {'children':[{'object':'block', 'type':'paragraph', 'paragraph':{'rich_text':[{'type':'text','text': {'content': content} }] }}]}
			requests.patch(global_vars.NOTION_CHILDREN_URL % response.json()['id'],json=task_content,headers=self.get_notion_headers())
		
		# Setup the response telegram message
		return "Created task with id [%s](%s). Status code: %s (%s)" % (response.json()['id'],response.json()['url'],response.status_code,response.reason)

	def set_weight(self,_message_text):
		journal = notion_journal(self.config)
		journal.add_weight(_message_text)

	# add a grocery to the grocery list
	def add_grocery(self,_grocery):
		new_grocery = {'children':[{'object':'block', 'type':'to_do', 'to_do':{'rich_text':[{'type':'text','text': {'content': _grocery} }] }}]}
		requests.patch(global_vars.NOTION_CHILDREN_URL % self.config.get_item('notion','GROCERIES_PAGE_KEY'),json=new_grocery,headers=self.get_notion_headers())
		return 'Added grocery: %s' % _grocery
		
	def get_groceries_url(self):
		return self.config.get_item('notion','GROCERIES_PAGE_URL')
		
	def set_grateful(self,_grateful_message):
		journal = notion_journal(self.config)
		return journal.set_grateful(_grateful_message)
		
	def set_goal(self,_goal):
		journal = notion_journal(self.config)
		return journal.set_goal(_goal)
	
	def get_daily_data(self):
		# Url for the notion call
		request_url = 'https://api.notion.com/v1/databases/%s/query' % self.config.get_item('notion','TASK_DATABASE_KEY')

		# Payload json to filter out done, dropped and not yet due tasks
		today = datetime.datetime.now().strftime("%Y-%m-%d")
		payload = {"filter": { "and": [{"property": "Status", "status" : { "does_not_equal": "Done 🙌" } },  { "property": "Status", "status" : { "does_not_equal": "Dropped 🔥" } }, {  "or": [ { "property":"Due date", "date" :{ "on_or_before":today } }, { "property":"Action date", "date" : { "on_or_before":today } } ] } ] } }

		# Get the notion stuff
		response = requests.post(request_url, json=payload,headers=self.get_notion_headers())
		
		print(response.content)
		
		result = "Good morning Niels, for today, there are a total of %s tasks:\n" % len(response.json()['results'])
		
		# Generate a list of tasks
		for task in response.json()['results']:
			if(task['properties']['Status']['status'] is None):
				result += "- %s (%s) \n" % (task['properties']['Name']['title'][0]['plain_text'],'no status')			
			else:
				result += "- %s (%s) \n" % (task['properties']['Name']['title'][0]['plain_text'],task['properties']['Status']['status']['name'])
		
		## *** Journal goal retrieving ***
		
		# Result should be added...
		journal = notion_journal(self.config)
		result += '\n\nToday\'s goal: %s' % journal.get_goal()
		
		return result
