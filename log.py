import logging
from Nconfig import config
from global_vars import global_vars

# Handles (correctly) logging of files, even when (for instance) an incorrect severity is given.
class log:
	
	config = config.config()
	
	# Get the config and initialise log
	def __init__(self):
		logging.basicConfig(filename=self.config.get_item('general','LOGFILE_NAME'), filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
	
	# return log file size
	def get_size(self):
		return sum(1 for _ in open(self.config.get_item('general','LOGFILE_NAME')))
		
	# returns human readabale message about the logfile name and size
	def get_size_message(self):
		return global_vars.LOG_LENGTH_MESSAGE % (self.config.get_item('general','LOGFILE_NAME'), self.get_size())
	
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