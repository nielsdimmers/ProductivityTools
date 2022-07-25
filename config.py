import configparser
import sys

# This class handles the config, prevents me using the init code quite a few times
class config:

	def __init__(self):
		if len(sys.argv) >= 3 and sys.argv[1]=='--config':
			configFile = sys.argv[2]
		else:
			configFile = 'config'
		
		# Parse the notion vars from the config file
		global configParser 
		configParser = configparser.RawConfigParser()
		configParser.read(configFile)
			
	def getItem(self,category,configItem):
		return (configParser.get(category,configItem))