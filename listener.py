from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import telegram
import notion_interface
import config
import log
from global_vars import global_vars
import datetime

# Telegram listener class to respond to telegram messages.
class Listener:

	config = config.config()
	log = log.log()

	# Telegram message escape a string
	def escape_string(self, _text_message):
		special_chars = {'\\':'\\\\','`':'&#96;','*':'\*','_':'\_','{':'\{','}':'\}','[':'\[',']':'\]','(':'\(',')':'\)','#':'\#','+':'\+','-':'\-','.':'\.','!':'\!','=':'\='}
		for special_key in special_chars:
			_text_message = _text_message.replace(special_key,special_chars[special_key])
		return _text_message

	def send_telegram_reply(self, update, _reply_message):
		try:
			update.message.reply_text(self.escape_string(_reply_message),quote=False,parse_mode=telegram.ParseMode.MARKDOWN_V2)
		except NetworkError as error:
			self.log.log('EXCEPTION', global_vars.TELEGRAM_SEND_ERROR % _reply_message)
			self.log.log('EXCEPTION', error)
		
	def grocery_list(self,update,notion):
		if len(update.message.text) > 3:
			notion_append_response = notion.add_grocery(update.message.text[3:])
			self.send_telegram_reply(update,notion_append_response)
		
		else:
			response = notion.get_groceries()
		
			# reply with the full groceries list
			message_reply = "**BOODSCHAPPEN**\n\n"
			for paragraph in response['results']:
				if paragraph['type'] == 'to_do': 
					message_reply += '[X] ' if paragraph['to_do']['checked'] else '[] '
				if len(paragraph[paragraph['type']]['rich_text']) > 0:
					message_reply += paragraph[paragraph['type']]['rich_text'][0]['plain_text']
				message_reply += "\n"

			message_reply += 'Grocerylist in notion: %s' % notion.get_groceries_url()
			self.send_telegram_reply(update,message_reply)

	def execute_command(self,update,context):
		if update.message.from_user.id != int(self.config.get_item('telegram','TELEGRAM_CHAT_ID')):
			self.log.log('WARNING', global_vars.USER_NOT_ALLOWED_ERROR % (update.message.from_user.name,update.message.from_user.id))
			return
		command = update.message.text.split(' ')[0][1:] # Split the message by space, get the first part and remove first character, e.g.: split the command from the message!
		notion = notion_interface.notion()
		
		if command == 'daily':
			self.send_telegram_reply(update, notion.get_daily_data())
		elif command == 'b':
			self.grocery_list(update,notion)
		elif command == 'tk':
			self.send_telegram_reply(update, notion.create_task(update.message.text[4:]))
		elif command == 'log':
			self.send_telegram_reply(update, self.log.get_size_message())
		elif command == 'week':
			self.send_telegram_reply(update, global_vars.DATETIME_WEEK_NUMBER % datetime.date.today().strftime("%W"))
			
	def main(self):
		updater = Updater(self.config.get_item('telegram','TELEGRAM_API_TOKEN'), use_context=True)
		dp = updater.dispatcher
		dp.add_handler(CommandHandler('daily',self.execute_command), True)
		dp.add_handler(CommandHandler('tk',self.execute_command), True)
		dp.add_handler(CommandHandler('b',self.execute_command), True)
		dp.add_handler(CommandHandler('log',self.execute_command), True)
		dp.add_handler(CommandHandler('week',self.execute_command), True)
		updater.start_polling()
		updater.idle()

if __name__ == '__main__':
	bot = Listener()
	bot.main()