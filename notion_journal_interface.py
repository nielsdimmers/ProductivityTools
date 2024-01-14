from datetime import datetime
import requests
from global_vars import global_vars
from config import config
import time
import json
import notion_json_builder

# Models a journal, which is created on init, or retrieved on init
class notion_journal:
		
	def get_notion_headers(self):
		return  notion_json_builder.NotionHeaders(self.config.get_item('notion','ACCESS_KEY')).__dict__
			
	def __init__(self,_date = datetime.now().strftime("%Y-%m-%d")): # creates a journal if it doesn't exist
		self.config = config.config('config_notion')
		response = requests.post(global_vars.NOTION_DATABASE_QUERY_URL % self.config.get_item('notion','GOAL_DATABASE_KEY'), json = json.loads(global_vars.NOTION_RETRIEVE_JOURNAL_JSON % (_date,_date)),headers=self.get_notion_headers())
		if len(response.json()['results']) > 0:
			self.journal_id = response.json()['results'][0]['id'] # journal exists, set the ID.
		else:
			journal_title = '%s %s' % (_date,global_vars.DAYS_OF_WEEK[datetime.strptime(_date, '%Y-%m-%d').weekday()]) # it doesn't exist, create the journal
			journal_content = notion_json_builder.NotionPage(self.config.get_item('notion','GOAL_DATABASE_KEY'),[journal_title],_date).__dict__
			
			self.journal_id = requests.post(global_vars.NOTION_PAGE_CREATE_URL, json=journal_content,headers=self.get_notion_headers()).json()['id'] # This line creates journal		
		self.retrieve_time = 0
		self.properties = requests.get(global_vars.NOTION_DATABASE_GET_URL % self.config.get_item('notion','GOAL_DATABASE_KEY'),headers=self.get_notion_headers()).json()['properties']
	
	def get_page(self): # Get the page, sets a timer to not keep retrieving it.
		if self.retrieve_time < (int(time.time()) - int(self.config.get_item('notion','MIN_RETRIEVE_TIME'))):
			self.page = requests.get(global_vars.NOTION_PAGE_URL % self.journal_id ,headers=self.get_notion_headers())
			self.retrieve_time = int(time.time())
		return self.page
	
	def get_url(self):
		return self.get_page().json()['url']
	
	def journal_property(self,_property,_value): 	# handles the journal property command, returns text
		if _value == "":
			return 'In journal dated %s, current %s is: %s' % (self.get_journal_property(global_vars.JOURNAL_DATE_KEY),_property,self.get_journal_property(_property))
		if self.set_journal_property(_property,_value).status_code == global_vars.HTTP_OK_CODE:
			return 'In journal dated %s, set %s to: %s' % (self.get_journal_property(global_vars.JOURNAL_DATE_KEY),_property, _value)
		return 'Error updating %s to value %s.' % (_property,_value)
	
	def count_words(self): # counts the number of words of the current journal
		result = 0
		for paragraph in requests.get(global_vars.NOTION_CHILDREN_URL  % self.journal_id, headers=self.get_notion_headers()).json()['results']:
			for text in paragraph[paragraph['type']]['rich_text']:
				result += len(text['plain_text'].split())
		self.set_journal_property(global_vars.JOURNAL_LENGTH_KEY,result)
		return result
	
	def set_journal_property(self,_property,_value): # Set a journal text property
		return requests.patch(global_vars.NOTION_PAGE_URL % self.journal_id, headers = self.get_notion_headers(),json=json.loads(global_vars.NOTION_PROPERTY_JSON[self.properties[_property]['type']] % (_property,_value)))
	
	def get_journal_property(self,_property):
		property_data = self.get_page().json()['properties'][_property]
		if property_data['type'] == 'date':
			return property_data['date']['start']
		elif property_data['type'] == 'rich_text':
			if len(property_data['rich_text']) > 0:
				return property_data['rich_text'][0]['plain_text']
		else:
			return property_data[property_data['type']]
			
	# Send the journal to the notion journal page
	def send_journal(self,_journal,time_stamp = True):
		journal_entry = ('(%s) %s' % (datetime.now().strftime("%H:%M:%S"),_journal)) if time_stamp else _journal
		journal_entry = journal_entry.replace('"','\\"')
		response = requests.patch(global_vars.NOTION_CHILDREN_URL % self.journal_id,json=json.loads(global_vars.NOTION_JOURNAL_JSON % journal_entry.strip()),headers=self.get_notion_headers())
		if response.status_code == global_vars.HTTP_OK_CODE:
			return global_vars.NOTION_JOURNAL_OK_MSG % (self.get_journal_property(global_vars.JOURNAL_DATE_KEY),len(_journal),len(_journal.split()))
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