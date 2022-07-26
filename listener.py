from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import telegram
import notion_interface
import requests
import config
import log
import global_vars

# Telegram listener class to respond to telegram messages.
class Listener:

	def __init__(self):
		global config
		config = config.config()

		global log
		log = log.log()

	# Telegram message escape a string
	def escape_string(self, _text_message):
		special_chars = {'\\':'\\\\','`':'&#96;','*':'\*','_':'\_','{':'\{','}':'\}','[':'\[',']':'\]','(':'\(',')':'\)','#':'\#','+':'\+','-':'\-','.':'\.','!':'\!','=':'\='}
		for special_key in special_chars:
			_text_message = _text_message.replace(special_key,special_chars[special_key])
		return _text_message

	def send_telegram_reply(self, update, _reply_message):
		update.message.reply_text(self.escape_string(_reply_message),quote=False,parse_mode=telegram.ParseMode.MARKDOWN_V2)
		
	def log_size(self,update,context):
		if update.message.from_user.id == int(config.get_item('telegram','TELEGRAM_CHAT_ID')):
			num_lines = sum(1 for _ in open(config.get_item('general','LOGFILE_NAME')))
			message = 'The logfile %s is %s lines long.' % (config.get_item('general','LOGFILE_NAME'), num_lines)
			self.send_telegram_reply(update,message)
		else:
			log.log('WARNING',USER_NOT_ALLOWED_ERROR % (update.message.from_user.name,update.message.from_user.id))
		
	def daily_data(self,update,context):
		if update.message.from_user.id == int(config.get_item('telegram','TELEGRAM_CHAT_ID')):
			self.send_telegram_reply(update, notion.get_daily_data())
		else:
			log.log('WARNING',USER_NOT_ALLOWED_ERROR % (update.message.from_user.name,update.message.from_user.id))
	
	def grocery_list(self,update,context):
		if update.message.from_user.id != int(config.get_item('telegram','TELEGRAM_CHAT_ID')):
			log.log('WARNING',USER_NOT_ALLOWED_ERROR % (update.message.from_user.name,update.message.from_user.id))
			return

		if len(update.message.text) > 3:
			notion_append_response = notion.add_grocery(update.message.text[3:])
			self.send_telegram_reply(update,notion_append_response)
		
		else:
			# The actual call		
			response = notion.get_groceries()
		
			# reply with the full groceries list
			message_reply = "**BOODSCHAPPEN**\n"
			for paragraph in response['results']:
				message_reply += "\n"
				todo_text = ""
				if len(paragraph[paragraph['type']]['rich_text']) > 0:
					todo_text += paragraph[paragraph['type']]['rich_text'][0]['plain_text']
				if paragraph['type'] == 'to_do': 
					message_reply += '[X] ' if paragraph['to_do']['checked'] else '[] '
				message_reply += todo_text

			message_reply += '\nGrocerylist in notion: %s' % notion.get_groceries_url()
			self.send_telegram_reply(update,message_reply)

	
	def new_task(self,update,context):
		# Check if it is me (just to be 100% sure nobody is messing with me)
		if update.message.from_user.id == int(config.get_item('telegram','TELEGRAM_CHAT_ID')):
			message_reply = notion.create_task(update.message.text[4:])
			self.send_telegram_reply(update,message_reply)
		else:
			log.log('WARNING',USER_NOT_ALLOWED_ERROR % (update.message.from_user.name,update.message.from_user.id))
	
	def main(self):
		global notion
		notion = notion_interface.notion(config)
		updater = Updater(config.get_item('telegram','TELEGRAM_API_TOKEN'), use_context=True)
		dp = updater.dispatcher
		dp.add_handler(CommandHandler('daily',self.daily_data), True)
		dp.add_handler(CommandHandler('tk',self.new_task), True)
		dp.add_handler(CommandHandler('b',self.grocery_list), True)
		dp.add_handler(CommandHandler('log',self.log_size), True)
		updater.start_polling()
		updater.idle()

if __name__ == '__main__':
	bot = Listener()
	bot.main()