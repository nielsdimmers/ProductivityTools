import sqlite3
import datetime
import time
import prettytable as pt
from config import config

class DomainCheck:


	def __init__(self):
		self.config = config.config('config_DomainCheck')
	
	def getQuery(self,query):
		# query database for information
		db_connection = sqlite3.connect(self.config.get_item('DomainCheck','DATABASE_FILE'))
		db_cursor = db_connection.cursor()
		
		table_output = [a for a in db_cursor.execute(query)]
		
		# Be sure to close the connection
		db_connection.close()
		
		return table_output
		
	# give a overview of the domains accessed in the last hours_to_look_back hours
	def domain_overview(self,hours_to_look_back = 24):
		if hours_to_look_back == '' or int(hours_to_look_back) == 0:
			hours_to_look_back = 24
		else:
			hours_to_look_back = int(hours_to_look_back)
		
		# get the required timestamp
		epochTime = int(time.time()) - (60*60*hours_to_look_back)
		
		table_output = self.getQuery('SELECT MIN(timestamp),MAX(timestamp),COUNT(*),domain FROM queries WHERE timestamp > %s GROUP BY domain ORDER BY COUNT(*) DESC LIMIT 25' % epochTime)
		
		# set up the table
		response_table = pt.PrettyTable(['Last accessed', 'Count', 'Domain'])
		response_table.align['Last accessed'] = 'l'
		response_table.align['Count'] = 'r'
		response_table.align['Domain'] = 'l'
		
		for line in table_output:
			last_date = datetime.datetime.fromtimestamp(line[1])
			response_table.add_row([last_date,line[2],line[3]])
		
		# generate the response
		response = 'Domains accessed in the last %s hour(s)\n' % hours_to_look_back
		
		response += '```\n%s\n```' % response_table
		
		return response
	
	# Give an overview of the clients requesting the given domain	
	def domain_check(self,domain):
		
		# Get the data from the database
		table_output = self.getQuery('SELECT MAX(queries.timestamp),COUNT(*),network_addresses.name,queries.client FROM queries,network_addresses WHERE network_addresses.ip = queries.client AND queries.domain = \'%s\' GROUP BY queries.client,network_addresses.name order by COUNT(*) DESC' % domain)
		
		# Make pretty table
		response_table = pt.PrettyTable(['last','count','name','ip'])
		
		for line in table_output:
			last_date = datetime.datetime.fromtimestamp(line[0])
			response_table.add_row([last_date,line[1],line[2],line[3]])
			response_table.align['ip'] = 'l'
			response_table.align['count'] = 'r'
			response_table.align['name'] = 'r'
	
		response = 'Clients accessing domain ```%s```\n' % domain
		
		response += '```\n%s\n```' % response_table
		
		return response
