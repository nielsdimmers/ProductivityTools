from telegram.ext import Application, Updater, InlineQueryHandler, CommandHandler, filters, MessageHandler
import telegram
import notion_interface
import config
import log
from global_vars import global_vars
from notion_journal_interface import notion_journal
import datetime

# Telegram listener class to respond to telegram messages.
class Listener:

	config = config.config()
	log = log.log()

	async def send_telegram_reply(self, update, _reply_message):
		try:
			await update.message.reply_text(_reply_message,quote=False, parse_mode='Markdown')
		except NetworkError as error:
			self.log.log('EXCEPTION', global_vars.TELEGRAM_SEND_ERROR % _reply_message)
			self.log.log('EXCEPTION', error)
		
	async def grocery_list(self,update,notion):
		message_reply = ""
		if len(update.message.text) > 3:
			message_reply = notion.add_grocery(update.message.text[3:])
		else:
			response = notion.get_groceries()
			for paragraph in response['results']:
				if paragraph['type'] == 'to_do' and len(paragraph[paragraph['type']]['rich_text']) > 0:
					if paragraph['to_do']['checked']:
						message_reply += '✅ _%s_\n' % paragraph[paragraph['type']]['rich_text'][0]['plain_text']
					else:
					 message_reply += '⬜️ %s\n' % paragraph[paragraph['type']]['rich_text'][0]['plain_text']
			message_reply += '[Grocerylist in notion](%s)' % notion.get_groceries_url()
		await self.send_telegram_reply(update,message_reply)

	async def execute_command(self,update,context):
		if update.message.from_user.id != int(self.config.get_item('telegram','TELEGRAM_CHAT_ID')):
			self.log.log('WARNING', global_vars.USER_NOT_ALLOWED_ERROR % (update.message.from_user.name,update.message.from_user.id))
			return
		command = update.message.text.split(' ')[0][1:] # split the command from the message!
		notion = notion_interface.notion()
		journal = notion_journal()
		
		if command == 'daily':
			await self.send_telegram_reply(update, notion.get_daily_data())
		elif command == 'b':
			await self.grocery_list(update,notion)
		elif command == 'tk':
			await self.send_telegram_reply(update, notion.create_task(update.message.text[4:]))
		elif command == 'log':
			await self.send_telegram_reply(update, self.log.get_size_message())
		elif command == 'week':
			await self.send_telegram_reply(update, global_vars.DATETIME_WEEK_NUMBER % datetime.date.today().strftime("%W"))
		elif command == 'weight':
			await self.send_telegram_reply(update, journal.journal_property('Gewicht (Kg)',update.message.text[8:]))
		elif command == 'grateful':
			await self.send_telegram_reply(update, journal.journal_property('Grateful',update.message.text[10:]))
		elif command == 'goal':
			await self.send_telegram_reply(update, journal.journal_property('Goal (commander\'s intent)',update.message.text[6:]))
	
	async def micro_journal(self, update, context):
		notion = notion_journal()
		await self.send_telegram_reply(update, notion.micro_journal(update.message.text))
	
	def main(self):
		application = Application.builder().token(self.config.get_item('telegram','TELEGRAM_API_TOKEN')).build()
		application.add_handler(CommandHandler('daily',self.execute_command), True)
		application.add_handler(CommandHandler('tk',self.execute_command), True)
		application.add_handler(CommandHandler('b',self.execute_command), True)
		application.add_handler(CommandHandler('log',self.execute_command), True)
		application.add_handler(CommandHandler('week',self.execute_command), True)
		application.add_handler(CommandHandler('weight',self.execute_command), True)
		application.add_handler(CommandHandler('grateful',self.execute_command), True)
		application.add_handler(CommandHandler('goal',self.execute_command), True)
		application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.micro_journal))
		application.run_polling()

if __name__ == '__main__':
	bot = Listener()
	bot.main()