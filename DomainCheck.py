import sqlite3
import datetime
import time
import prettytable as pt
from config import config

class DomainCheck:


	def __init__(self):
		self.config = config.config('config_DomainCheck')
		
	def checkDomain(self,hours_to_look_back = 24):
		if hours_to_look_back == '':
			hours_to_look_back = 24
		else:
			hours_to_look_back = int(hours_to_look_back)
		
		
		# get the required timestamp
		epochTime = int(time.time()) - (60*60*hours_to_look_back)
		
		db_connection = sqlite3.connect(self.config.get_item('DomainCheck','DATABASE_FILE'))
		db_cursor = db_connection.cursor()
		
		table_output = [a for a in db_cursor.execute('SELECT MIN(timestamp),MAX(timestamp),COUNT(*),domain FROM queries WHERE timestamp > %s GROUP BY domain ORDER BY COUNT(*) DESC LIMIT 10' % epochTime)]
		
		# Be sure to close the connection
		db_connection.close()
		
		
		response_table = pt.PrettyTable(['Last acessed', 'Count', 'Domain'])
		response_table.align['Last acessed'] = 'l'
		response_table.align['count'] = 'r'
		response_table.align['Domain'] = 'l'
		
		for line in table_output:
			last_date = datetime.datetime.fromtimestamp(line[1])
			response_table.add_row([last_date,line[2],line[3]])
			
		response = 'Domains accessed in the last %s hour(s)\n' % hours_to_look_back
		
		response += '```\n%s\n```' % response_table
		
		return response
	

