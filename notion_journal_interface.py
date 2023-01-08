import datetime
import requests
from global_vars import global_vars
import config

# Models a journal, which is created on init, or retrieved on init
class notion_journal:
	
	config = config.config('config_notion')
	
	journal_id = ""
	
	def get_notion_headers(self):
		return {'Authorization': 'Bearer %s' % self.config.get_item('notion','ACCESS_KEY'), 'Content-Type':'application/json','Notion-Version':'2022-02-22'}
	
	# creates a journal if it doesn't exist
	def __init__(self,_config_parser):
		today = datetime.datetime.now().strftime("%Y-%m-%d")
				
		payload = {"filter": { "or" : [ { "property" : "title", "title" : { "starts_with" : today } }, { "property" : "Datum", "date" : { "equals" : today } } ] } }
		
		request_url = 'https://api.notion.com/v1/databases/%s/query' % self.config.get_item('notion','GOAL_DATABASE_KEY')
		
		response = requests.post(request_url, json = payload,headers=self.get_notion_headers())

		# Controleer of jounal is aangemaakt
		if len(response.json()['results']) > 0:
			self.journal_id = response.json()['results'][0]['id'] # journal bestaat, geef ID terug
		else:
			journal_title = '%s %s' % (today,global_vars.DAYS_OF_WEEK[datetime.datetime.now().weekday()]) # hij bestaat niet, maak hem aan
			journal_content = {'parent':{'database_id':self.config.get_item('notion','GOAL_DATABASE_KEY')}, 'properties':{'title':{'title':[{"text":{"content":journal_title}}]},'Datum':{'date':{'start':today}}}}
			response = requests.post('https://api.notion.com/v1/pages', json=journal_content,headers=self.get_notion_headers()) # Deze regel maakt de journal aan
			self.journal_id = response.json()['id']
	
	def set_grateful(self,_grateful_message):
		if _grateful_message == "":
			return 'Today, you are grateful for: %s.' % self.get_grateful()
		else:
			return self.set_journal_property('Grateful',_grateful_message)
		
	def get_grateful(self):
		request_url = 'https://api.notion.com/v1/pages/%s' % self.journal_id
		response = requests.get(request_url ,headers=self.get_notion_headers())
		if len(response.json()['properties']['Grateful']['rich_text']) > 0:
			return response.json()['properties']['Grateful']['rich_text'][0]['plain_text']
		else:
			return 'no grateful message defined'
	
	# Set a journal text property
	def set_journal_property(self,_property,_value):
		request_url = 'https://api.notion.com/v1/pages/%s' % self.journal_id
		return_message = {'properties': { _property : {'rich_text': [{'text': {'content' : _value}}]}}}
		response = requests.patch(request_url, headers = self.get_notion_headers(),json=return_message)
		response = requests.get(request_url ,headers=self.get_notion_headers())
		retrieved_value = response.json()['properties'][_property]['rich_text'][0]['plain_text']
		
		result = ''
		if(retrieved_value == _value):
			result = 'Set %s to \'%s\'' % (_property, retrieved_value)
		else:
			result = '%s update failed, value is %s' % (_property, retrieved_value)
		return result
	
	# Add a micro journal entry, with the current time.
	def micro_journal(self,_journal):
		journal_entry = '(%s) %s' % (datetime.datetime.now().strftime("%H:%M:%S"),_journal)
		request_url = 'https://api.notion.com/v1/pages/%s' % self.journal_id
		new_journal = {'children':[{'object':'block', 'type':'paragraph', 'paragraph':{'rich_text':[{'type':'text','text': {'content': journal_entry} }] }}]}
		response = requests.patch(global_vars.NOTION_CHILDREN_URL % self.journal_id,json=new_journal,headers=self.get_notion_headers())
		result = ''
		if response.status_code == 200:
			result = 'Micro journal added.'
		else:
			result = 'Error response code %s. Full json follows: \n%s' % (response.status_code, response.json())
		return result
	
	# 
	def set_goal(self,_goal):
		if _goal == "":
			return 'The current goal is: %s' % self.get_goal()
		else:
			return self.set_journal_property('Goal (commander\'s intent)',_goal)
	
	# Get the goal, always retrieves the journal because it could be updated.
	def get_goal(self):
		request_url = 'https://api.notion.com/v1/pages/%s' % self.journal_id
		response = requests.get(request_url ,headers=self.get_notion_headers())
		if len(response.json()['properties']['Goal (commander\'s intent)']['rich_text']) > 0:
			return response.json()['properties']['Goal (commander\'s intent)']['rich_text'][0]['plain_text']
		else:
			return 'no goal defined'
		