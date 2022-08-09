import configparser
import sys

# This class handles the config, prevents me using the init code quite a few times
class config:

	config_parser = configparser.RawConfigParser()

	def __init__(self,filename='config'): # 2022-08-07 Allows for different filenames
		
		config_file = ""
		
		if len(sys.argv) >= 3 and sys.argv[1]=='--config':
			cmd_filename = sys.argv[2]
			if(cmd_filename[-6:] == 'config'):
				cmd_filename = cmd_filename[:-6]
			config_file = cmd_filename + filename
		else:
			config_file = filename
		
		# Parse the notion vars from the config file
		self.config_parser.read(config_file)
		
	def get_sections(self):
		return self.config_parser.sections()
			
	def get_item(self,category,_config_item):
		return (self.config_parser.get(category,_config_item))