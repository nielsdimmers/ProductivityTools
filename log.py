import logging
import config

# Handles (correctly) logging of files, even when (for instance) an incorrect severity is given.
class log:
	
	# Get the config and initialise log
	def __init__(self):
		global config
		config = config.config()
		
		logging.basicConfig(filename=config.getItem('general','LOGFILE_NAME'), filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
	
	# Log the actual message
	def log(self,severity="INFO",message="no message provided"):
		severity = severity.upper()
		severity_dict = {
			"DEBUG": logging.debug,
			"INFO" : logging.info,
			"WARNING": logging.warning,
			"ERROR": logging.error,
			"CRITICAL": logging.critical
		}
		if severity in severity_dict:
			function = severity_dict[severity]
			function(message)	
		else:
			logging.error("Severity '%s' for message '%s' is an invalid severity." % (severity,message) )