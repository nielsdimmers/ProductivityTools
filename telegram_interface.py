from telegram.ext import Application, Updater, InlineQueryHandler, CommandHandler, filters, MessageHandler
from config import config
from global_vars import global_vars
import log
import asyncio

# Interface with telegram
class telegram_interface:
	
	def __init__(self):
		self.config = config.config()
		self.application = Application.builder().token(self.config.get_item('telegram','TELEGRAM_API_TOKEN')).build()
		self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
		self.log = log.log()
	
	# Send a text message using the default configuration
	def send_message(self, message):
		chat_id = self.config.get_item('telegram','TELEGRAM_CHAT_ID')
		asyncio.get_event_loop().run_until_complete(self.application.bot.send_message(chat_id=chat_id,text=message))
	
	# return an image
	# image is the image buffer to return
	def send_image(self,image):
		chat_id = self.config.get_item('telegram','TELEGRAM_CHAT_ID')
		asyncio.get_event_loop().run_until_complete(self.application.bot.send_photo(chat_id=chat_id, photo=image))
	
	# reply to a message with text, only used internally
	async def send_reply(self,update,_reply_message):
		try:
			await update.message.reply_text(_reply_message,quote=False, parse_mode='Markdown')
		except Exception as error:
			self.log.log('EXCEPTION', global_vars.TELEGRAM_SEND_ERROR % (_reply_message,error))
	
	# handle a message, usually by adding a journal entry
	async def handle_message(self,update,context):
		response = self.command_handler.journal(update.message.text)
		await self.send_reply(update,response)
	
	# calls the commandhandler
	async def handle_command(self,update,context):
		# this is where we split the command from the textbit, and just send the command and the text to the commandhandler.
		self.updater = update
		if update.message.from_user.id != int(self.config.get_item('telegram','TELEGRAM_CHAT_ID')):
			self.log.log('WARNING', global_vars.USER_NOT_ALLOWED_ERROR % (update.message.from_user.name,update.message.from_user.id))
			return
		command = update.message.text.split(' ')[0][1:] # split the command from the message!
		message = '' if len(update.message.text) <= len(command) + 1 else update.message.text[(len(command)+2):]
		return_message = self.command_handler.execute(command,message)
		if len(return_message) > 0:
			await self.send_reply(update,return_message)
	
	# add a command to the list of possible commands
	def add_command(self,command,command_handler):
		self.command_handler = command_handler
		self.application.add_handler(CommandHandler(command,self.handle_command), True)
	
	# the listener which listens to commands or journal input
	def start_listener(self,welcome_message):
		self.send_message(welcome_message)
		self.application.run_polling()
		