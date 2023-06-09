from telegram.ext import Application, Updater, InlineQueryHandler, CommandHandler, filters, MessageHandler
import telegram
import notion_interface
from config import config
import log
from global_vars import global_vars
from notion_journal_interface import notion_journal
import datetime
import asyncio

# Telegram listener class to respond to telegram messages.
class Listener:

	def __init__(self):
		self.config = config.config()
		self.log = log.log()

	async def send_telegram_reply(self, update, _reply_message):
		try:
			await update.message.reply_text(_reply_message,quote=False, parse_mode='Markdown')
		except Exception as error:
			self.log.log('EXCEPTION', global_vars.TELEGRAM_SEND_ERROR % (_reply_message,error))
		
	def grocery_list(self,_message,notion):
		if len(_message) > 0:
			return notion.add_grocery(_message)
		message_reply = ''
		for paragraph in notion.get_groceries()['results']:
			if paragraph['type'] == 'to_do' and len(paragraph[paragraph['type']]['rich_text']) > 0:
				message_reply += ('✅' if paragraph['to_do']['checked'] else '⬜️') + paragraph[paragraph['type']]['rich_text'][0]['plain_text'] + '\n'
		message_reply += '\n[Grocerylist in notion](%s)' % notion.get_groceries_url()
		return message_reply

	async def execute_command(self,update,context):
		if update.message.from_user.id != int(self.config.get_item('telegram','TELEGRAM_CHAT_ID')):
			self.log.log('WARNING', global_vars.USER_NOT_ALLOWED_ERROR % (update.message.from_user.name,update.message.from_user.id))
			return
		command = update.message.text.split(' ')[0][1:] # split the command from the message!
		message = '' if len(update.message.text) <= len(command) + 1 else update.message.text[(len(command)+2):]
		notion = notion_interface.notion()
		journal = notion_journal(datetime.datetime.now().strftime("%Y-%m-%d"))
		
		if command == 'daily':
			await self.send_telegram_reply(update, notion.get_daily_data())
		elif command == 'b':
			await self.send_telegram_reply(update,self.grocery_list(message,notion))
		elif command == 'tk':
			await self.send_telegram_reply(update, notion.create_task(message))
		elif command == 'log':
			await self.send_telegram_reply(update, self.log.get_size_message())
		elif command == 'week':
			await self.send_telegram_reply(update, global_vars.DATETIME_WEEK_NUMBER % datetime.date.today().strftime("%W"))
		elif command == 'weight':
			await self.send_telegram_reply(update, journal.journal_property(global_vars.JOURNAL_WEIGHT_KEY,message))
		elif command == 'grateful':
			await self.send_telegram_reply(update, journal.journal_property(global_vars.JOURNAL_GRATEFUL_KEY,message))
		elif command == 'goal':
			await self.send_telegram_reply(update, journal.journal_property(global_vars.JOURNAL_GOAL_KEY,message))
		elif command == 'tomgoal':
			tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
			await self.send_telegram_reply(update, notion_journal(tomorrow).journal_property(global_vars.JOURNAL_GOAL_KEY,message))
		elif command == 'legal':
			await self.send_telegram_reply(update, global_vars.LEGAL_NOTICE)
		
	
	async def micro_journal(self, update, context):
		notion = notion_journal()
		await self.send_telegram_reply(update, notion.micro_journal(update.message.text))
	
	def main(self):
		application = Application.builder().token(self.config.get_item('telegram','TELEGRAM_API_TOKEN')).build()
		telegram_commands = ['daily','tk','b','log','week','weight','grateful','goal','tomgoal','legal']
		for telegram_command in telegram_commands:
			application.add_handler(CommandHandler(telegram_command,self.execute_command), True)
		application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.micro_journal))
		asyncio.get_event_loop().run_until_complete(application.bot.send_message(chat_id=self.config.get_item('telegram','TELEGRAM_CHAT_ID'),text=global_vars.REBOOT_MESSAGE))
		application.run_polling()