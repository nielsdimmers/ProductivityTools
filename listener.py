import configparser
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import telegram
import sys
import notionInterface
import requests

# Telegram listener class to respond to telegram messages.
class Listener:

	def __init__(self):
		if len(sys.argv) >= 3 and sys.argv[1]=='--config':
			configFile = sys.argv[2]
		else:
			configFile = 'config'

		# Parse the notion vars from the config file
		global configParser 
		configParser = configparser.RawConfigParser()
		configParser.read(configFile)

	# Telegram message escape a string
	def escapeString(self, textMessage):
		specialChars = {'\\':'\\\\','`':'&#96;','*':'\*','_':'\_','{':'\{','}':'\}','[':'\[',']':'\]','(':'\(',')':'\)','#':'\#','+':'\+','-':'\-','.':'\.','!':'\!','=':'\='}
		for specialKey in specialChars:
			textMessage = textMessage.replace(specialKey,specialChars[specialKey])
		return textMessage

	def sendTelegramReply(self, update, replyMessage):
		update.message.reply_text(self.escapeString(replyMessage),quote=False,parse_mode=telegram.ParseMode.MARKDOWN_V2)
		
	def dailyData(self,update,context):
		self.sendTelegramReply(update, notion.getDailyData())
	
	def groceryList(self,update,context):
		if update.message.from_user.id != int(configParser.get('telegram','TELEGRAM_CHAT_ID')):
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
		if update.message.from_user.id == int(configParser.get('telegram','TELEGRAM_CHAT_ID')):
			messageReply = notion.createTask(update.message.text[4:])

			self.sendTelegramReply(update,messageReply)
	
	def main(self):
		global notion
		notion = notionInterface.notion(configParser)
		updater = Updater(configParser.get('telegram','TELEGRAM_API_TOKEN'), use_context=True)
		dp = updater.dispatcher
		dp.add_handler(CommandHandler('daily',self.dailyData), True)
		dp.add_handler(CommandHandler('tk',self.newTask), True)
		dp.add_handler(CommandHandler('b',self.groceryList), True)
		updater.start_polling()
		updater.idle()

if __name__ == '__main__':
	bot = Listener()
	bot.main()