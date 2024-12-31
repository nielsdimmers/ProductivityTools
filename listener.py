import notion_interface
from config import config
from global_vars import global_vars
from notion_journal_interface import notion_journal
import datetime
import log

# Telegram listener class to respond to telegram messages.
class Listener:

	def __init__(self, _message_interface):
		self.config = config.config()
		self.log = log.log()
		self.message_interface = _message_interface

	def execute(self,command,message):
		notion = notion_interface.notion()
		journal = notion_journal(datetime.datetime.now().strftime("%Y-%m-%d"))

		if command == 'daily':
			return notion.get_daily_data()
		elif command == 'inbox':
			return notion.create_task(message)
		elif command == 'log':
			return self.log.get_size_message()
		elif command == 'd':
			return notion.create_dysfunction(message)
		elif command == 'week':
			return global_vars.DATETIME_WEEK_NUMBER % datetime.date.today().strftime("%W")
		elif command == 'weight':
			return journal.journal_property(global_vars.JOURNAL_WEIGHT_KEY,message)
		elif command == 'legal':
			return global_vars.LEGAL_NOTICE
		elif command == 'drink':
			return journal.journal_property(global_vars.JOURNAL_DRINK_KEY,message)
		elif command == 'words':
			words = journal.count_words()
			notion_config = config.config('config_notion')
			percentage = round((words/int(notion_config.get_item('notion','JOURNAL_DESIRED_LENGTH'))) * 100,2)
			return global_vars.NOTION_JOURNAL_LENGTH_MSG % (words,percentage,notion_config.get_item('notion','JOURNAL_DESIRED_LENGTH'))
	
	def journal(self, message):
		notion = notion_journal(datetime.datetime.now().strftime("%Y-%m-%d"))
		return notion.micro_journal(message)
	
	def main(self):
		telegram_commands = ['daily','inbox','log','week','weight','legal','words','d','drink']
		for telegram_command in telegram_commands:
			self.message_interface.add_command(telegram_command,self)
		self.message_interface.start_listener(global_vars.REBOOT_MESSAGE)