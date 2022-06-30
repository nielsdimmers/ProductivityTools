import configparser
from telegram.ext import Application, InlineQueryHandler, CommandHandler
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

	async def sendTelegramReply(self, update, replyMessage):
		await update.message.reply_text(replyMessage,quote=False)
		
	async def dailyData(self,update,context):
		await self.sendTelegramReply(update, notion.getDailyData())
	
	async def groceryList(self,update,context):
		if update.message.from_user.id != int(configParser.get('telegram','TELEGRAM_CHAT_ID')):
			return
		pageKey = configParser.get('notion','GROCERIES_PAGE_KEY')

		if len(update.message.text) > 3:
			notionAppendResponse = notion.addGrocery(update.message.text[3:])
			await self.sendTelegramReply(update,notionAppendResponse)
		
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

			messageReply += '\nGrocerylist in notion: %s' % configParser.get('notion','GROCERIES_PAGE_URL')
			await self.sendTelegramReply(update,messageReply)

	
	async def newTask(self,update,context):
		# Check if it is me (just to be 100% sure nobody is messing with me)
		if update.message.from_user.id == int(configParser.get('telegram','TELEGRAM_CHAT_ID')):
			messageReply = notion.createTask(update.message.text[4:])

			await self.sendTelegramReply(update,messageReply)
	
	def main(self):
		global notion
		notion = notionInterface.notion(configParser)
		application = Application.builder().token(configParser.get('telegram','TELEGRAM_API_TOKEN')).build()
		application.add_handler(CommandHandler('daily',self.dailyData), True)
		application.add_handler(CommandHandler('tk',self.newTask), True)
		application.add_handler(CommandHandler('b',self.groceryList), True)
		application.run_polling()

if __name__ == '__main__':
	bot = Listener()
	bot.main()