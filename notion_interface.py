from notion_abstract import notion_abstract
from global_vars import global_vars
from notion_journal_interface import notion_journal
import json
import notion_json_builder
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
	
	def create_dysfunction(self,_dysfunction_title):
		dictionary = notion_json_builder.NotionPage(super().get_config('DYSFUNCTION_DATABASE_KEY'),[_dysfunction_title]).__dict__
		# The creation of the task
		response = super().post_notion('page','',dictionary)
		
		# Setup the response telegram message
		return "Did nothing %s " % response.status_code

	# get task count based on the notion style date
	def get_task_count(self,date):	
		response = super().post_notion('database',super().get_config('TASK_DATABASE_KEY'),json.loads(global_vars.NOTION_TASKLIST_QUERY_JSON % (date,date)))
		return len(response.json()['results'])
	
	def get_open_task_count(self):
		response = super().post_notion('database',super().get_config('TASK_DATABASE_KEY'),json.loads(global_vars.NOTION_OPEN_TASK_QUERY_JSON))
		return len(response.json()['results'])
	
	def get_open_task_effort(self):
		response = super().post_notion('database',super().get_config('TASK_DATABASE_KEY'),json.loads(global_vars.NOTION_OPEN_TASK_QUERY_JSON))
		total_effort = 0
		for task in response.json()['results']:
			if task['properties']['AI Effort (number)']['formula']['type'] == 'number':
				total_effort += task['properties']['AI Effort (number)']['formula']['number']
		return total_effort

	def get_daily_data(self):
		# number of words of yesterday's journal
		yesterday = (date.today() - timedelta(days = 1)).strftime("%Y-%m-%d")
		yesterday_journal = notion_journal(yesterday)
		today = datetime.now().strftime("%Y-%m-%d")
		today_journal = notion_journal(today)

		result = 'Good morning Niels, yesterday\'s journal word count is %s.\n' % yesterday_journal.count_words()
		
		result += "For today, there are a total of %s tasks.\n" % self.get_task_count(today)

		open_task_count = self.get_open_task_count()
		open_effort_sum = self.get_open_task_effort()

		today_journal.set_property(global_vars.JOURNAL_OPEN_TASKS_COUNT_KEY,open_task_count)
		today_journal.set_property(global_vars.JOURNAL_OPEN_TASKS_ESTIMATE_KEY,open_effort_sum)

		result += "In total, there are %s open tasks which represent an effort of %s .\n\n" % (open_task_count,open_effort_sum)

		return result