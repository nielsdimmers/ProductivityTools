import argparse
import datetime
from config import config
from global_vars import global_vars
from listener import Listener
from mailcheck import mailcheck
from notion_journal_interface import notion_journal
import notion_interface
from telegram_interface import telegram_interface
from text_interface import text_interface
from report import report
from log import log

class script_handler:

	def __init__(self,interface):
		self.config = config.config()
		# let's take the telegram interface as default
		
		if interface == 'telegram':
			self.message_interface = telegram_interface()
		elif interface == 'text':
			# otherwise the text interface
			self.message_interface = text_interface()
	
	def get_message_interface(self):
		return self.message_interface
		
	def log_count(self):
		self.message_interface.send_message(log().get_size_message())
		
	def send_message(self,message):
		self.message_interface.send_message(message)
	
	def daily(self):
		self.message_interface.send_message(notion_interface.notion().get_daily_data())
		self.message_interface.send_image(report().send_graph())
		
	def words(self):
		journal_length = notion_journal(datetime.datetime.now().strftime("%Y-%m-%d")).count_words()
		notion_config = config.config('config_notion')
		journal_length_percentage = (journal_length/int(notion_config.get_item('notion','JOURNAL_DESIRED_LENGTH'))) * 100
		message = global_vars.NOTION_JOURNAL_LENGTH_MSG % (journal_length,journal_length_percentage,notion_config.get_item('notion','JOURNAL_DESIRED_LENGTH'))
		self.message_interface.send_message(message)

# This bit of code is all to enable proper commandline argument handling.
parser = argparse.ArgumentParser(description=global_vars.SCRIPT_DESCRIPTION)
parser.add_argument('action', help=global_vars.SCRIPT_ACTION_USAGE)
parser.add_argument('--interface','-i',help=global_vars.SCRIPT_INTERFACE_USAGE, default='telegram')
args = parser.parse_args()
action = args.action
interface = args.interface

# This is the instance of the handler (class above)
handler = script_handler(interface)

# Determine the action and execute it
if action == 'daily':
	handler.daily()
elif action == 'logcount':
	handler.log_count()
elif action == 'mailcheck':
	mailcheck().check_mail()
elif action == 'listener':
	Listener(handler.get_message_interface()).main()
elif action == 'legal':
	handler.send_message(global_vars.LEGAL_NOTICE)
elif action == 'words':
	handler.words()
else:
	handler.send_message(global_vars.SCRIPT_USAGE)