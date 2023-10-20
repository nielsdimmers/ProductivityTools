from telegram.ext import Application, Updater, InlineQueryHandler, CommandHandler, filters, MessageHandler
import telegram
import notion_interface
from config import config
import log
from global_vars import global_vars
from notion_journal_interface import notion_journal
import datetime
import asyncio
from DomainCheck import DomainCheck

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
		elif command == 'tk':
			await self.send_telegram_reply(update, notion.create_task(message))
		elif command == 'log':
			await self.send_telegram_reply(update, self.log.get_size_message())
		elif command == 'week':
			await self.send_telegram_reply(update, global_vars.DATETIME_WEEK_NUMBER % datetime.date.today().strftime("%W"))
		elif command == 'weight':
			await self.send_telegram_reply(update, journal.journal_property(global_vars.JOURNAL_WEIGHT_KEY,message))
		elif command == 'goal':
			await self.send_telegram_reply(update, journal.journal_property(global_vars.JOURNAL_GOAL_KEY,message))
		elif command == 'tomgoal':
			tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
			await self.send_telegram_reply(update, notion_journal(tomorrow).journal_property(global_vars.JOURNAL_GOAL_KEY,message))
		elif command == 'legal':
			await self.send_telegram_reply(update, global_vars.LEGAL_NOTICE)
		elif command == 'words':
			words = journal.count_words()
			notion_config = config.config('config_notion')
			percentage = round((words/int(notion_config.get_item('notion','JOURNAL_DESIRED_LENGTH'))) * 100,2)
			await self.send_telegram_reply(update, global_vars.NOTION_JOURNAL_LENGTH_MSG % (words,percentage,notion_config.get_item('notion','JOURNAL_DESIRED_LENGTH')))
		elif command == 'onepercent':
			await self.send_telegram_reply(update, journal.journal_property(global_vars.JOURNAL_ONE_PERCENT_KEY,message))
		elif command == 'domainoverview':
			checker = DomainCheck()
			await self.send_telegram_reply(update, checker.domain_overview(message))
		elif command == 'domain':
			checker = DomainCheck()
			await self.send_telegram_reply(update, checker.domain_check(message))
	
	async def micro_journal(self, update, context):
		notion = notion_journal(datetime.datetime.now().strftime("%Y-%m-%d"))
		await self.send_telegram_reply(update, notion.micro_journal(update.message.text))
	
	def main(self):
		application = Application.builder().token(self.config.get_item('telegram','TELEGRAM_API_TOKEN')).build()
		telegram_commands = ['daily','tk','log','week','weight','goal','tomgoal','legal','words','onepercent','domainoverview','domain']
		for telegram_command in telegram_commands:
			application.add_handler(CommandHandler(telegram_command,self.execute_command), True)
		application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.micro_journal))
		asyncio.get_event_loop().run_until_complete(application.bot.send_message(chat_id=self.config.get_item('telegram','TELEGRAM_CHAT_ID'),text=global_vars.REBOOT_MESSAGE))
		application.run_polling()