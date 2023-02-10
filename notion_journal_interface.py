import datetime
import requests
from global_vars import global_vars
import config
import time

# Models a journal, which is created on init, or retrieved on init
class notion_journal:
	
	config = config.config('config_notion')
	
	journal_id = ""
	
	page = {}
	
	retrieve_time = 0
	
	def get_notion_headers(self):
		return {'Authorization': 'Bearer %s' % self.config.get_item('notion','ACCESS_KEY'), 'Content-Type':'application/json','Notion-Version':'2022-02-22'}
	
	# creates a journal if it doesn't exist
	def __init__(self,_date =''):
		today = datetime.datetime.now().strftime("%Y-%m-%d") if _date == '' else _date
		payload = {"filter": { "or" : [ { "property" : "title", "title" : { "starts_with" : today } }, { "property" : "Datum", "date" : { "equals" : today } } ] } }
		request_url = 'https://api.notion.com/v1/databases/%s/query' % self.config.get_item('notion','GOAL_DATABASE_KEY')
		response = requests.post(request_url, json = payload,headers=self.get_notion_headers())
		if len(response.json()['results']) > 0:
			self.journal_id = response.json()['results'][0]['id'] # journal bestaat, geef ID terug
		else:
			journal_title = '%s %s' % (today,global_vars.DAYS_OF_WEEK[datetime.datetime.now().weekday()]) # hij bestaat niet, maak hem aan
			journal_content = {'parent':{'database_id':self.config.get_item('notion','GOAL_DATABASE_KEY')}, 'properties':{'title':{'title':[{"text":{"content":journal_title}}]},'Datum':{'date':{'start':today}}}}
			response = requests.post('https://api.notion.com/v1/pages', json=journal_content,headers=self.get_notion_headers()) # Deze regel maakt de journal aan
			self.journal_id = response.json()['id']
	
	def get_page(self):
		if self.retrieve_time < (int(time.time()) - 3):
			request_url = 'https://api.notion.com/v1/pages/%s' % self.journal_id
			self.page = requests.get(request_url ,headers=self.get_notion_headers())
			self.retrieve_time = int(time.time())
		return self.page
	
	# handles the journal property command, returns text
	def journal_property(self,_property,_value):
		if _value == "":
			return 'Current %s is: %s' % (_property,self.get_journal_property(_property))
		else:
			result = self.set_journal_property(_property,_value)
			if result.status_code == 200:
				return 'Set %s to: %s' % (_property, _value)
			else:
				return 'Error updating %s to value %s.' % (_property,_value)
	
	# counts the number of words of the current journal
	def count_words(self):
		request_url = 'https://api.notion.com/v1/blocks/%s/children' % self.journal_id
		response = requests.get(request_url, headers=self.get_notion_headers())
		result = 0;
		for paragraph in response.json()['results']:
			for text in paragraph[paragraph['type']]['rich_text']:
				result += len(text['plain_text'].split())
		self.set_journal_property('Journal length',result)
		return result
	
	# Set a journal text property
	def set_journal_property(self,_property,_value):
		request_url = 'https://api.notion.com/v1/pages/%s' % self.journal_id
		return_message = {}
		property_type = self.get_property_type(_property)
		if property_type == 'rich_text':
			return_message = {'properties': { _property : {'rich_text': [{'text': {'content' : _value}}]}}}
		elif property_type == 'number':
			return_message = {'properties': { _property : {'number':float(_value)}}}
		response = requests.patch(request_url, headers = self.get_notion_headers(),json=return_message)
		return response
	
	def get_property_type(self,_property):
		return self.get_page().json()['properties'][_property]['type']
	
	def get_journal_property(self,_property):
		response = self.get_page()
		property_type = self.get_property_type(_property)
		if property_type == 'rich_text':
			if len(response.json()['properties'][_property]['rich_text']) > 0:
				return response.json()['properties'][_property]['rich_text'][0]['plain_text']
		elif property_type == 'number':
			return response.json()['properties'][_property]['number']
	
	# Send the journal to the notion journal page
	def send_journal(self,_journal,time_stamp = True):
		if time_stamp:
			journal_entry = '(%s) %s' % (datetime.datetime.now().strftime("%H:%M:%S"),_journal)
		else:
			journal_entry = _journal	
		request_url = 'https://api.notion.com/v1/pages/%s' % self.journal_id
		new_journal = {'children':[{'object':'block', 'type':'paragraph', 'paragraph':{'rich_text':[{'type':'text','text': {'content': journal_entry} }] }}]}
		response = requests.patch(global_vars.NOTION_CHILDREN_URL % self.journal_id,json=new_journal,headers=self.get_notion_headers())
		if response.status_code == 200:
			return 'Micro journal with length %s characters and %s words added.\n' % (len(_journal),len(_journal.split()))
		else:
			return 'Error response code %s. Full json follows: \n%s\n' % (response.status_code, response.json())
				
	# Add a micro journal entry, with the current time.
	def micro_journal(self,_journal):
		result = ''
		if len(_journal) > 1000:
			result += self.send_journal('Multi part journal entry follows:')
			for part in _journal.split('\n'):
				if part == '\n' or part == '' or part == '\r': # skip over empty lines
					continue
				result += self.send_journal(part, time_stamp = False)
		else:
			result += self.send_journal(_journal)

		return result
		
		
		
		
		
		
		
		
		
		