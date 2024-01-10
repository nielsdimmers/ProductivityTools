from notion_interface import notion
from notion_journal_interface import notion_journal
import datetime
from global_vars import global_vars
import random
from data_interface import data_interface

class daily:
	
	# return a random journal prompt
	def get_journal_prompt(self):
		file_path = './journal_prompts.txt'
		# Open the file in read mode
		with open(file_path, 'r') as file:
		# Read lines and store them in a list
			lines = file.readlines()
		return lines[random.randint(1,len(lines))-1].strip()
			
	def get_daily_data(self):
		# number of words of yesterday's journal
		yesterday = (datetime.date.today() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")
		yesterday_journal = notion_journal(yesterday)
		today = datetime.datetime.now().strftime("%Y-%m-%d")
		
		result = 'Good morning Niels, yesterday\'s journal word count is %s.\n' % yesterday_journal.count_words()

		journal = notion_journal()
		
		ai_uses = data_interface().get_data_count(yesterday)
		
		result += 'You used the AI bot %s times yesterday.\n' % ai_uses
		
		journal.set_journal_property(global_vars.JOURNAL_AICOUNT_KEY,ai_uses)
		
		# Get the notion stuff
		task_count = notion().get_task_count(today)
		
		result += "For today, there are a total of %s tasks.\n\n" % task_count

		journal_prompt = journal.get_journal_property(global_vars.JOURNAL_PROMPT_KEY)
		
		if journal_prompt == None:
			journal_prompt = self.get_journal_prompt()
			journal.set_journal_property(global_vars.JOURNAL_PROMPT_KEY,journal_prompt)
		result += "Your journal prompt for today is: %s" % journal_prompt
		
		result += '\n\nToday\'s goal is %s. [Today\'s journal](%s)' % (journal.get_journal_property(global_vars.JOURNAL_GOAL_KEY),journal.get_url())
		
		return result