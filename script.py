import requests
import notion_interface
import urllib.parse
import sys
from config import config
from global_vars import global_vars
import log
from test_journal import test_journal
from listener import Listener
from mailcheck import mailcheck
from notion_journal_interface import notion_journal
import datetime

class script_handler:

	def __init__(self):
		self.config = config.config()

	def log_count(self):
		requests.get(global_vars.TELEGRAM_MSG_URL % (self.config.get_item('telegram','TELEGRAM_API_TOKEN'),self.config.get_item('telegram','TELEGRAM_CHAT_ID'),urllib.parse.quote(log.log().get_size_message())))

	def daily(self):
		requests.get(global_vars.TELEGRAM_MSG_URL % (self.config.get_item('telegram','TELEGRAM_API_TOKEN'),self.config.get_item('telegram','TELEGRAM_CHAT_ID'),urllib.parse.quote(notion_interface.notion().get_daily_data())))
		
	def words (self):
		journal_length = notion_journal(datetime.datetime.now().strftime("%Y-%m-%d")).count_words()
		notion_config = config.config('config_notion')
		journal_length_percentage = (journal_length/int(notion_config.get_item('notion','JOURNAL_DESIRED_LENGTH'))) * 100
		message = global_vars.JOURNAL_LENGTH_MESSAGE % (journal_length,journal_length_percentage,notion_config.get_item('notion','JOURNAL_DESIRED_LENGTH'))
		requests.get(global_vars.TELEGRAM_MSG_URL % (self.config.get_item('telegram','TELEGRAM_API_TOKEN'),self.config.get_item('telegram','TELEGRAM_CHAT_ID'),urllib.parse.quote(message)))
	
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print(global_vars.SCRIPT_USAGE)
	elif sys.argv[1] == 'daily':
		script_handler().daily()
	elif sys.argv[1] == 'logcount':
		script_handler().log_count()
	elif sys.argv[1] == 'test':
		test_journal().run_test()
	elif sys.argv[1] == 'mailcheck':
		mailcheck().check_mail()
	elif sys.argv[1] == 'listener':
		Listener().main()
	elif sys.argv[1] == 'legal':
		print(global_vars.LEGAL_NOTICE)
	elif sys.argv[1] == 'words':
		script_handler().words()
	else:
		print(global_vars.SCRIPT_USAGE)