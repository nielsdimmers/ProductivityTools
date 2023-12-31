from config import config
from global_vars import global_vars
import log

# Interface with telegram
class text_interface:
	
	def __init__(self):
		self.config = config.config()
		self.log = log.log()
		self.command_list = []
	
	# Send a text message using the default configuration
	def send_message(self, message):
		print(message)
			
	# return an image
	# image is the image buffer to return
	def send_image(self,image):
		self.send_message(global_vars.IMAGE_TEXT_REPLACEMENT)
	
	# reply to a message with text, only used internally
	def send_reply(self,_reply_message):
		self.send_message(_reply_message)
			
	# handle a message, usually by adding a journal entry
	def handle_message(self,journal):
		response = self.command_handler.journal(journal)
		self.send_message(response)
	
	# calls the commandhandler
	def handle_command(self,message):
		command = message.split(' ')[0][1:] # split the command from the message!
		return_message = ''
		if command == 'quit':
			self.send_message(global_vars.QUIT_MESSAGE)
			self.running = False
		elif command in self.command_list:
			message = '' if len(message) <= len(command) + 1 else message[(len(command)+2):]
			return_message = self.command_handler.execute(command,message)
		else:
			return_message = self.handle_message(message) # it's not a command, so it's journal.
		if return_message is not None and len(return_message) > 0:
			self.send_reply(return_message)
	
	# add a command to the list of possible commands
	def add_command(self,command,command_handler):
		self.command_list.append(command)
		self.command_handler = command_handler
	
	# the listener which listens to commands or journal input
	def start_listener(self,welcome_message):
		self.send_message(welcome_message)
		self.running = True
		while self.running:
			user_input = input()
			self.handle_command(user_input)