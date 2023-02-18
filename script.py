# script.py
import requests
import notion_interface
import urllib.parse
import sys
from Nconfig import config
from global_vars import global_vars
import log
from test_journal import test_journal

config = config.config()
notion = notion_interface.notion()
log = log.log()

def log_count():
	requests.get(global_vars.TELEGRAM_MSG_URL % (config.get_item('telegram','TELEGRAM_API_TOKEN'),config.get_item('telegram','TELEGRAM_CHAT_ID'),urllib.parse.quote(log.get_size_message())))

def daily():
	requests.get(global_vars.TELEGRAM_MSG_URL % (config.get_item('telegram','TELEGRAM_API_TOKEN'),config.get_item('telegram','TELEGRAM_CHAT_ID'),urllib.parse.quote(notion.get_daily_data())))
	
if __name__ == '__main__':
	if len(sys.argv) != 2:
		print(global_vars.SCRIPT_USAGE)
	elif sys.argv[1] == 'daily':
		daily()
	elif sys.argv[1] == 'logcount':
		log_count()
	elif sys.argv[1] == 'test':
		tester = test_journal()
		tester.run_test()