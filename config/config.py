import configparser
import sys

# This class handles the config, prevents me using the init code quite a few times
class config:

	config_parser = configparser.RawConfigParser()

	def __init__(self,filename='config'): # 2022-08-07 Allows for different filenames
		
		# Get the directory bit of the command, and append the folder name to it.
		config_file = sys.argv[0][:sys.argv[0].rfind('/')] if '/' in sys.argv[0] else '.'
		config_file += '/config/%s' % filename
		
		# Parse the notion vars from the config file
		self.config_parser.read(config_file)
		
	def get_sections(self):
		return self.config_parser.sections()
			
	def get_item(self,category,_config_item):
		return (self.config_parser.get(category,_config_item))