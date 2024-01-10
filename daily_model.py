from notion_interface import notion
from notion_journal_interface import notion_journal
import datetime
from global_vars import global_vars
import random

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
		yesterday_journal = notion_journal((datetime.date.today() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d"))
		today = datetime.datetime.now().strftime("%Y-%m-%d")
		
		result = 'Good morning Niels, yesterday\'s journal word count is %s.\n' % yesterday_journal.count_words()
		
		# Get the notion stuff
		task_count = notion().get_task_count(today)
		
		result += "For today, there are a total of %s tasks.\n\n" % task_count

		journal = notion_journal()
		journal_prompt = journal.get_journal_property(global_vars.JOURNAL_PROMPT_KEY)
		
		if journal_prompt == None:
			journal_prompt = self.get_journal_prompt()
			journal.set_journal_property(global_vars.JOURNAL_PROMPT_KEY,journal_prompt)
		result += "Your journal prompt for today is: %s" % journal_prompt
		
		result += '\n\nToday\'s goal is %s. [Today\'s journal](%s)' % (journal.get_journal_property(global_vars.JOURNAL_GOAL_KEY),journal.get_url())
		
		return result
		
daily = daily()
print(daily.get_daily_data())