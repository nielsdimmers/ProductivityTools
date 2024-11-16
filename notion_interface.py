from notion_abstract import notion_abstract
from global_vars import global_vars
from notion_journal_interface import notion_journal
import json
import notion_json_builder
import random
import sys
import os
from datetime import datetime, date, timedelta


# Notion interface to interact with notion
class notion(notion_abstract):
		
	# create a task object based on the given title
	def create_task(self,_task_data):
		
		task_data = _task_data.split('\n') # Split the task data by the delimiter defining between title [0] and the contents [1..*]
	
		dictionary = notion_json_builder.NotionPage(super().get_config('INBOX_DATABASE_KEY'),[task_data.pop(0)]).__dict__

		# The creation of the task
		response = super().post_notion('page','',dictionary)
		super().patch_notion('children',response.json()['id'],notion_json_builder.NotionChildren(task_data).__dict__)
		
		# Setup the response telegram message
		
		return "Created inbox item with title '[%s](%s)'. Status code: %s (%s)" % (response.json()['properties']['Name']['title'][0]['plain_text'],response.json()['url'],response.status_code,response.reason)	
	
	# get task count based on the notion style date
	def get_task_count(self,date):	
		response = super().post_notion('database',super().get_config('TASK_DATABASE_KEY'),json.loads(global_vars.NOTION_TASKLIST_QUERY_JSON % (date,date)))
		return len(response.json()['results'])
		
	# return the currently active evening checklist task
	def get_checklist_url(self, _checklist_type):
		request_json = ''
		if _checklist_type == global_vars.EVENING:
			request_json = global_vars.NOTION_TASKLIST_EVENING_JSON
		if _checklist_type == global_vars.MORNING:
			request_json = global_vars.NOTION_TASKLIST_MORNING_JSON
		if _checklist_type == global_vars.AFTERNOON:
			request_json = global_vars.NOTION_TASKLIST_AFTERNOON_JSON			
		response = super().post_notion('database',super().get_config('TASK_DATABASE_KEY'),json.loads(request_json))
		return response.json()['results'][0]['url']
	
	def get_daily_data(self):
		# number of words of yesterday's journal
		yesterday = (date.today() - timedelta(days = 1)).strftime("%Y-%m-%d")
		yesterday_journal = notion_journal(yesterday)
		today = datetime.now().strftime("%Y-%m-%d")
		
		result = 'Good morning Niels, yesterday\'s journal word count is %s.\n' % yesterday_journal.count_words()
		
		result += "For today, there are a total of %s tasks.\n\n" % self.get_task_count(today)
		
		return result