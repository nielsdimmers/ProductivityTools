import configparser
import requests
import datetime
from global_vars import global_vars
from notion_journal_interface import notion_journal
from config import config
import json

# Notion interface to interact with notion
class notion:

	def __init__(self): # see update 63 in readme why this is needed.
		self.config = config.config('config_notion')

	# Returns the headers of the notion message
	def get_notion_headers(self):
		return {'Authorization': 'Bearer %s' % self.config.get_item('notion','ACCESS_KEY'), 'Content-Type':'application/json','Notion-Version':'2022-06-28'}
	
	# Returns the JSON part of the groceries page
	def get_groceries(self):
		response = requests.get(global_vars.NOTION_CHILDREN_URL % self.config.get_item('notion','GROCERIES_PAGE_KEY') ,headers=self.get_notion_headers())
		return response.json()
	
	# create a task object based on the given title
	def create_task(self,_task_data):
		
		task_data = _task_data.split('\n') # Split the task data by the delimiter defining between title [0] and the contents [1..*]
		dictionary = {'parent':{'database_id':self.config.get_item('notion','INBOX_DATABASE_KEY')}, 'properties':{'title':{'title':[{"text":{"content":task_data[0]}}]}}}

		# The creation of the task
		response = requests.post('https://api.notion.com/v1/pages', json=dictionary,headers=self.get_notion_headers())
		task_data.pop(0) ## remove the title from the array
		
		for content in task_data:
			task_content = {'children':[{'object':'block', 'type':'paragraph', 'paragraph':{'rich_text':[{'type':'text','text': {'content': content} }] }}]}
			requests.patch(global_vars.NOTION_CHILDREN_URL % response.json()['id'],json=task_content,headers=self.get_notion_headers())
		
		# Setup the response telegram message
		return "Created task with id [%s](%s). Status code: %s (%s)" % (response.json()['id'],response.json()['url'],response.status_code,response.reason)

	# add a grocery to the grocery list
	def add_grocery(self,_grocery):
		new_grocery = {'children':[{'object':'block', 'type':'to_do', 'to_do':{'rich_text':[{'type':'text','text': {'content': _grocery} }] }}]}
		requests.patch(global_vars.NOTION_CHILDREN_URL % self.config.get_item('notion','GROCERIES_PAGE_KEY'),json=new_grocery,headers=self.get_notion_headers())
		return 'Added grocery: %s' % _grocery
		
	def get_groceries_url(self):
		return self.config.get_item('notion','GROCERIES_PAGE_URL')
	
	# Add a micro journal entry
	def micro_journal(self,_journal):
		return notion_journal(self.config).micro_journal(_journal)
	
	def get_daily_data(self):
		# number of words of yesterday's journal
		yesterday_journal = notion_journal((datetime.date.today() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d"))
		today = datetime.datetime.now().strftime("%Y-%m-%d")
		
		result = 'Good morning Niels, yesterday\'s journal word count is %s.\n' % yesterday_journal.count_words()
		
		# Get the notion stuff
		response = requests.post('https://api.notion.com/v1/databases/%s/query' % self.config.get_item('notion','TASK_DATABASE_KEY'), json=json.loads(global_vars.NOTION_TASKLIST_QUERY_JSON % (today,today)),headers=self.get_notion_headers())
		
		result += "For today, there are a total of %s tasks:\n" % len(response.json()['results'])
		
	 	#	Generate a list of tasks
		for task in response.json()['results']:
			status = 'no status' if task['properties']['Status']['status'] is None else task['properties']['Status']['status']['name']
			result += "- [%s](%s) (%s) \n" % (task['properties']['Name']['title'][0]['plain_text'],task['url'],status)
		
		journal = notion_journal()
		result += '\n\nToday\'s goal is %s. [Today\'s journal](%s)' % (journal.get_journal_property(global_vars.JOURNAL_GOAL_KEY),journal.get_url())
		
		return result