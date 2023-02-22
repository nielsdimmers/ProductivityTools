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

class script_handler:

	def __init__(self):
		self.config = config.config()

	def log_count(self):
		requests.get(global_vars.TELEGRAM_MSG_URL % (self.config.get_item('telegram','TELEGRAM_API_TOKEN'),self.config.get_item('telegram','TELEGRAM_CHAT_ID'),urllib.parse.quote(log.log().get_size_message())))

	def daily(self):
		requests.get(global_vars.TELEGRAM_MSG_URL % (self.config.get_item('telegram','TELEGRAM_API_TOKEN'),self.config.get_item('telegram','TELEGRAM_CHAT_ID'),urllib.parse.quote(notion_interface.notion().get_daily_data())))
	
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
	else:
		print(global_vars.SCRIPT_USAGE)