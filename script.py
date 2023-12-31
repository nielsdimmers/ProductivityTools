import notion_interface
import sys
from config import config
from global_vars import global_vars
import log
from listener import Listener
from mailcheck import mailcheck
from notion_journal_interface import notion_journal
import datetime
from telegram_interface import telegram_interface
import asyncio
import report

class script_handler:

	def __init__(self):
		self.config = config.config()
		self.message_interface = telegram_interface()
		
	def log_count(self):
		self.message_interface.send_message(log.log().get_size_message())

	def daily(self):
		self.message_interface.send_message(notion_interface.notion().get_daily_data())
		self.message_interface.send_image(report.report().send_graph())
		
	def words(self):
		journal_length = notion_journal(datetime.datetime.now().strftime("%Y-%m-%d")).count_words()
		notion_config = config.config('config_notion')
		journal_length_percentage = (journal_length/int(notion_config.get_item('notion','JOURNAL_DESIRED_LENGTH'))) * 100
		message = global_vars.NOTION_JOURNAL_LENGTH_MSG % (journal_length,journal_length_percentage,notion_config.get_item('notion','JOURNAL_DESIRED_LENGTH'))
		self.message_interface.send_message(message)
	
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print(global_vars.SCRIPT_USAGE)
	elif sys.argv[1] == 'daily':
		script_handler().daily()
	elif sys.argv[1] == 'logcount':
		script_handler().log_count()
	elif sys.argv[1] == 'mailcheck':
		mailcheck().check_mail()
	elif sys.argv[1] == 'listener':
		Listener().main()
	elif sys.argv[1] == 'legal':
		print(global_vars.LEGAL_NOTICE)
	elif sys.argv[1] == 'words':
		script_handler.words()
	else:
		print(global_vars.SCRIPT_USAGE)