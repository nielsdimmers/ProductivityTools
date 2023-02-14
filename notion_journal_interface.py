import datetime
import requests
from global_vars import global_vars
from Nconfig import config
import time
import json

# Models a journal, which is created on init, or retrieved on init
class notion_journal:
	
	config = config.config('config_notion')
	journal_id = ""
	page = {}
	properties = {}
	retrieve_time = 0
	
	def get_notion_headers(self):
		return {'Authorization': 'Bearer %s' % self.config.get_item('notion','ACCESS_KEY'), "accept": "application/json",'Notion-Version':'2022-06-28'}
	
	# creates a journal if it doesn't exist
	def __init__(self,_date =''):
		journal_date = datetime.datetime.now().strftime("%Y-%m-%d") if _date == '' else _date
		response = requests.post(global_vars.NOTION_DATABASE_QUERY_URL % self.config.get_item('notion','GOAL_DATABASE_KEY'), json = json.loads(global_vars.NOTION_RETRIEVE_JOURNAL_JSON % (journal_date,journal_date)),headers=self.get_notion_headers())
		if len(response.json()['results']) > 0:
			self.journal_id = response.json()['results'][0]['id'] # journal exists, set the ID.
		else:
			journal_title = '%s %s' % (journal_date,global_vars.DAYS_OF_WEEK[datetime.datetime.strptime(journal_date, '%Y-%m-%d').weekday()]) # it doesn't exist, create the journal
			journal_content = {'parent':{'database_id':self.config.get_item('notion','GOAL_DATABASE_KEY')}, 'properties':{'title':{'title':[{"text":{"content":journal_title}}]},'Datum':{'date':{'start':journal_date}}}}
			self.journal_id = requests.post(global_vars.NOTION_PAGE_CREATE_URL, json=journal_content,headers=self.get_notion_headers()).json()['id'] # This line creates journal		
		self.properties = requests.get(global_vars.NOTION_DATABASE_GET_URL % self.config.get_item('notion','GOAL_DATABASE_KEY'),headers=self.get_notion_headers()).json()['properties']
	
	def get_page(self):
		if self.retrieve_time < (int(time.time()) - int(self.config.get_item('notion','MIN_RETRIEVE_TIME'))):
			self.page = requests.get(global_vars.NOTION_PAGE_URL % self.journal_id ,headers=self.get_notion_headers())
			self.retrieve_time = int(time.time())
		return self.page
	
	# USE WITH CAUTION!
	def delete_journal(self):
		if self.get_journal_property('Korte samenvatting').split()[0] == self.config.get_item('notion','TEST_DATE'): # To make sure this class can only delete the test page
			requests.patch(global_vars.NOTION_PAGE_URL % self.journal_id ,json=json.loads('{"archived" : true}'),headers=self.get_notion_headers())

	# handles the journal property command, returns text
	def journal_property(self,_property,_value):
		if _value == "":
			return 'Current %s is: %s' % (_property,self.get_journal_property(_property))
		if self.set_journal_property(_property,_value).status_code == global_vars.HTTP_OK_CODE:
			return 'Set %s to: %s' % (_property, _value)
		return 'Error updating %s to value %s.' % (_property,_value)
	
	# counts the number of words of the current journal
	def count_words(self):
		result = 0
		for paragraph in requests.get(global_vars.NOTION_CHILDREN_URL  % self.journal_id, headers=self.get_notion_headers()).json()['results']:
			for text in paragraph[paragraph['type']]['rich_text']:
				result += len(text['plain_text'].split())
		self.set_journal_property('Journal length',result)
		return result
	
	# Set a journal text property
	def set_journal_property(self,_property,_value):
		return requests.patch(global_vars.NOTION_PAGE_URL % self.journal_id, headers = self.get_notion_headers(),json=json.loads(global_vars.NOTION_PROPERTY_JSON[self.properties[_property]['type']] % (_property,_value)))
	
	def get_journal_property(self,_property):
		result = requests.get(global_vars.NOTION_PROPERTY_GET_URL % (self.journal_id,self.properties[_property]['id']),headers=self.get_notion_headers())
		if result.json()['object'] == 'property_item':
			return result.json()[result.json()['type']]
		elif len(result.json()['results']) > 0:
			return result.json()['results'][0][result.json()['results'][0]['type']]['plain_text']
			
	# Send the journal to the notion journal page
	def send_journal(self,_journal,time_stamp = True):
		journal_entry = ('(%s) %s' % (datetime.datetime.now().strftime("%H:%M:%S"),_journal)) if time_stamp else _journal
		journal_entry = journal_entry.replace('"','\\"')
		response = requests.patch(global_vars.NOTION_CHILDREN_URL % self.journal_id,json=json.loads(global_vars.NOTION_JOURNAL_JSON % journal_entry),headers=self.get_notion_headers())
		if response.status_code == global_vars.HTTP_OK_CODE:
			return global_vars.NOTION_JOURNAL_OK_MSG % (len(_journal),len(_journal.split()))
		else:
			return global_vars.NOTION_JOURNAL_NOK_MSG % (response.status_code, response.json())
				
	# Add a micro journal entry
	def micro_journal(self,_journal):
		result = ''
		time_stamp_message = True
		if len(_journal.split('\n')) > 1:
			result += self.send_journal(global_vars.NOTION_JOURNAL_MULTIPART_ENTRY)
			time_stamp_message = False
		for part in _journal.split('\n'):
			if part == '' or part == '\r': # skip over empty lines
				continue
			result += self.send_journal(part, time_stamp = time_stamp_message)
		return result
		
		
		
		
		
		
		
		
		
		