from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import telegram
import notionInterface
import requests
import config
import log

# Telegram listener class to respond to telegram messages.
class Listener:

	def __init__(self):
		global config
		config = config.config()

		global log
		log = log.log()

	# Telegram message escape a string
	def escapeString(self, textMessage):
		specialChars = {'\\':'\\\\','`':'&#96;','*':'\*','_':'\_','{':'\{','}':'\}','[':'\[',']':'\]','(':'\(',')':'\)','#':'\#','+':'\+','-':'\-','.':'\.','!':'\!','=':'\='}
		for specialKey in specialChars:
			textMessage = textMessage.replace(specialKey,specialChars[specialKey])
		return textMessage

	def sendTelegramReply(self, update, replyMessage):
		update.message.reply_text(self.escapeString(replyMessage),quote=False,parse_mode=telegram.ParseMode.MARKDOWN_V2)
		
	def logSize(self,update,context):
		if update.message.from_user.id == int(config.getItem('telegram','TELEGRAM_CHAT_ID')):
			numLines = sum(1 for line in open(config.getItem('general','LOGFILE_NAME')))
			message = 'The logfile %s is %s lines long.' % (config.getItem('general','LOGFILE_NAME'), numLines)
			self.sendTelegramReply(update,message)
		else:
			log.log('WARNING','User name %s (id:%s) has no permission to send messages to this bot.' % (update.message.from_user.name,update.message.from_user.id))
		
	def dailyData(self,update,context):
		if update.message.from_user.id == int(config.getItem('telegram','TELEGRAM_CHAT_ID')):
			self.sendTelegramReply(update, notion.getDailyData())
		else:
			log.log('WARNING','User name %s (id:%s) has no permission to send messages to this bot.' % (update.message.from_user.name,update.message.from_user.id))
	
	def groceryList(self,update,context):
		if update.message.from_user.id != int(config.getItem('telegram','TELEGRAM_CHAT_ID')):
			log.log('WARNING','User name %s (id:%s) has no permission to send messages to this bot.' % (update.message.from_user.name,update.message.from_user.id))
			return

		if len(update.message.text) > 3:
			notionAppendResponse = notion.addGrocery(update.message.text[3:])
			self.sendTelegramReply(update,notionAppendResponse)
		
		else:
			# The actual call		
			response = notion.getGroceries()
		
			# reply with the full groceries list
			messageReply = "**BOODSCHAPPEN**\n"
			for paragraph in response['results']:
				messageReply += "\n"
				paragraphType = paragraph['type']
				todoText = ""
				if len(paragraph[paragraphType]['rich_text']) > 0:
					todoText += paragraph[paragraphType]['rich_text'][0]['plain_text']
				if paragraphType == 'to_do': 
					messageReply += '[X] ' if paragraph['to_do']['checked'] else '[] '
				messageReply += todoText

			messageReply += '\nGrocerylist in notion: %s' % notion.getGroceriesURL()
			self.sendTelegramReply(update,messageReply)

	
	def newTask(self,update,context):
		# Check if it is me (just to be 100% sure nobody is messing with me)
		if update.message.from_user.id == int(config.getItem('telegram','TELEGRAM_CHAT_ID')):
			messageReply = notion.createTask(update.message.text[4:])
			self.sendTelegramReply(update,messageReply)
		else:
			log.log('WARNING','User name %s (id:%s) has no permission to send messages to this bot.' % (update.message.from_user.name,update.message.from_user.id))
	
	def main(self):
		global notion
		notion = notionInterface.notion(config)
		updater = Updater(config.getItem('telegram','TELEGRAM_API_TOKEN'), use_context=True)
		dp = updater.dispatcher
		dp.add_handler(CommandHandler('daily',self.dailyData), True)
		dp.add_handler(CommandHandler('tk',self.newTask), True)
		dp.add_handler(CommandHandler('b',self.groceryList), True)
		dp.add_handler(CommandHandler('log',self.logSize), True)
		updater.start_polling()
		updater.idle()

if __name__ == '__main__':
	bot = Listener()
	bot.main()