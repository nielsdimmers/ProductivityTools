import configparser
import sys

# This class handles the config, prevents me using the init code quite a few times
class config:

	def __init__(self):
		if len(sys.argv) >= 3 and sys.argv[1]=='--config':
			_config_file = sys.argv[2]
		else:
			_config_file = 'config'
		
		# Parse the notion vars from the config file
		global configParser 
		configParser = configparser.RawConfigParser()
		configParser.read(_config_file)
			
	def get_item(self,category,_config_item):
		return (configParser.get(category,_config_item))