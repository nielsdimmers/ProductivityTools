from notion_abstract import notion_abstract
from datetime import datetime
from global_vars import global_vars
import time
import json
import notion_json_builder

# Models a journal, which is created on init, or retrieved on init
class notion_journal(notion_abstract):
					
	def __init__(self,_date = datetime.now().strftime("%Y-%m-%d")): # creates a journal if it doesn't exist
		super().__init__()
		response = super().post_notion('database',super().get_config('GOAL_DATABASE_KEY'), json.loads(global_vars.NOTION_RETRIEVE_JOURNAL_JSON % (_date,_date)))
		if len(response.json()['results']) > 0:
			self.journal_id = response.json()['results'][0]['id'] # journal exists, set the ID.
		else:
			journal_title = '%s %s' % (_date,global_vars.DAYS_OF_WEEK[datetime.strptime(_date, '%Y-%m-%d').weekday()]) # it doesn't exist, create the journal
			journal_content = notion_json_builder.NotionPage(super().get_config('GOAL_DATABASE_KEY'),[journal_title],_date).__dict__
			
			self.journal_id = super().post_notion('page',super().get_config('GOAL_DATABASE_KEY'),journal_content).json()['id'] # This line creates journal		
		self.retrieve_time = 0
		self.properties = super().get_notion('database',super().get_config('GOAL_DATABASE_KEY')).json()['properties']
	
	@property
	def page(self): # Get the page, sets a timer to not keep retrieving it.
		if self.retrieve_time < (int(time.time()) - int(super().get_config('MIN_RETRIEVE_TIME'))):
			self._page = super().get_notion('page',self.journal_id)
			self.retrieve_time = int(time.time())
		return self._page
	
	def get_url(self):
		return self.page.json()['url']
	
	def journal_property(self,_property,_value): 	# handles the journal property command, returns text
		if _value == "":
			return 'In journal dated %s, current %s is: %s' % (self.get_property(global_vars.JOURNAL_DATE_KEY),_property,self.get_property(_property))
		if self.set_property(_property,_value).status_code == global_vars.HTTP_OK_CODE:
			return 'In journal dated %s, set %s to: %s' % (self.get_property(global_vars.JOURNAL_DATE_KEY),_property, _value)
		return 'Error updating %s to value %s.' % (_property,_value)
	
	def count_words(self): # counts the number of words of the current journal
		result = 0
		for paragraph in super().get_notion('children',self.journal_id):
			for text in paragraph[paragraph['type']]['rich_text']:
				result += len(text['plain_text'].split())
		self.set_property(global_vars.JOURNAL_LENGTH_KEY,result)
		return result
	
	def set_property(self,_property,_value): # Set a journal text property
		return super().patch_notion('page',self.journal_id,json.loads(global_vars.NOTION_PROPERTY_JSON[self.properties[_property]['type']] % (_property,_value)))
	
	def get_property(self,_property):
		property_data = self.page.json()['properties'][_property]
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
		response = super().patch_notion('children',self.journal_id,json.loads(global_vars.NOTION_JOURNAL_JSON % journal_entry.strip()))
		if response.status_code == global_vars.HTTP_OK_CODE:
			return global_vars.NOTION_JOURNAL_OK_MSG % (self.get_property(global_vars.JOURNAL_DATE_KEY),len(_journal),len(_journal.split()))
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
			if part in ['', '\r']: continue
			result += self.send_journal(part, time_stamp = time_stamp_message)
		return result