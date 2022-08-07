import configparser
import sys

# This class handles the config, prevents me using the init code quite a few times
class config:

	configParser = configparser.RawConfigParser()

	def __init__(self,filename='config'): # 2022-08-07 Allows for different filenames
		
		if len(sys.argv) >= 3 and sys.argv[1]=='--config':
			cmdFilename = sys.argv[2]
			if(cmdFilename.endsWith('config')):
				cmdFilename = cmdFilename[:-6]
				config_file = cmdFilename + filename
		else:
			config_file = filename
		
		# Parse the notion vars from the config file
		self.configParser.read(config_file)
		
	def get_sections(self):
		return self.configParser.sections()
			
	def get_item(self,category,_config_item):
		return (self.configParser.get(category,_config_item))