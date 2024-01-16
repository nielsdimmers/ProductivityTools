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
		return "Created task with id [%s](%s). Status code: %s (%s)" % (response.json()['id'],response.json()['url'],response.status_code,response.reason)	
	
	# get task count based on the notion style date
	def get_task_count(self,date):	
		response = super().post_notion('database',super().get_config('TASK_DATABASE_KEY'),json.loads(global_vars.NOTION_TASKLIST_QUERY_JSON % (date,date)))
		return len(response.json()['results'])
	
	# get the data count for date
	def get_ai_data_count(self,date):
		response = super().post_notion('database',super().get_config('AI_USAGE_DATABASE_KEY'),notion_json_builder.NotionCreateDateFilter(date).__dict__)
		print('single page is %s\n\n' % response.json()['results'][0])
		return len(response.json()['results'])
		
	# return a random journal prompt
	def get_journal_prompt(self):
		with open(('%s/journal_prompts.txt' % os.path.dirname(sys.argv[0])), 'r') as file:
			lines = file.readlines()
		return lines[random.randint(1,len(lines))-1].strip()
			
	def get_daily_data(self):
		# number of words of yesterday's journal
		yesterday = (date.today() - timedelta(days = 1)).strftime("%Y-%m-%d")
		yesterday_journal = notion_journal(yesterday)
		today = datetime.now().strftime("%Y-%m-%d")
		
		result = 'Good morning Niels, yesterday\'s journal word count is %s.\n' % yesterday_journal.count_words()

		journal = notion_journal(today)
		
		ai_uses = self.get_ai_data_count(yesterday)
		result += 'You used the AI bot %s times yesterday.\n' % ai_uses
		
		result += 'Summary of yesterday\'s journal is:\n%s\n\n' % yesterday_journal.get_property(global_vars.JOURNAL_SUMMARY_KEY)
		
		yesterday_journal.set_property(global_vars.JOURNAL_AICOUNT_KEY,ai_uses)
		
		# Make an AI hit.
		dictionary = notion_json_builder.NotionPage(super().get_config('AI_USAGE_DATABASE_KEY'),['Created by Prod Tools bot']).__dict__
		dictionary['properties'].update(json.loads(global_vars.NOTION_AIBOT_JSON))
		response = super().post_notion('page','',dictionary)
		
		result += "For today, there are a total of %s tasks.\n\n" % self.get_task_count(today)

		journal_prompt = journal.get_property(global_vars.JOURNAL_PROMPT_KEY)
		
		if journal_prompt == None:
			journal_prompt = self.get_journal_prompt()
			journal.set_property(global_vars.JOURNAL_PROMPT_KEY,journal_prompt)
		result += "Your journal prompt for today is: %s" % journal_prompt
		
		result += '\n\nToday\'s goal is %s. [Today\'s journal](%s)' % (journal.get_property(global_vars.JOURNAL_GOAL_KEY),journal.get_url())
		
		return result