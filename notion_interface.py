import requests
from global_vars import global_vars
from notion_journal_interface import notion_journal
from config import config
import json
import notion_json_builder


# Notion interface to interact with notion
class notion:

	def __init__(self): # see update 63 in readme why this is needed.
		self.config = config.config('config_notion')

	# Returns the headers of the notion message
	def get_notion_headers(self):
		return  notion_json_builder.NotionHeaders(self.config.get_item('notion','ACCESS_KEY')).__dict__
		
	# create a task object based on the given title
	def create_task(self,_task_data):
		
		task_data = _task_data.split('\n') # Split the task data by the delimiter defining between title [0] and the contents [1..*]
	
		dictionary = notion_json_builder.NotionPage(self.config.get_item('notion','INBOX_DATABASE_KEY'),[task_data.pop(0)]).__dict__

		# The creation of the task
		response = requests.post('https://api.notion.com/v1/pages', json=dictionary,headers=self.get_notion_headers())
		
		task_content = notion_json_builder.NotionChildren(task_data).__dict__
		requests.patch(global_vars.NOTION_CHILDREN_URL % response.json()['id'],json=task_content,headers=self.get_notion_headers())
		
		# Setup the response telegram message
		return "Created task with id [%s](%s). Status code: %s (%s)" % (response.json()['id'],response.json()['url'],response.status_code,response.reason)	
	
	# Add a micro journal entry
	def micro_journal(self,_journal):
		return notion_journal(self.config).micro_journal(_journal)
	
	# get task count based on the notion style date
	def get_task_count(self,date):
		response = requests.post('https://api.notion.com/v1/databases/%s/query' % self.config.get_item('notion','TASK_DATABASE_KEY'), json=json.loads(global_vars.NOTION_TASKLIST_QUERY_JSON % (date,date)),headers=self.get_notion_headers())
		return len(response.json()['results'])