import datetime
import requests
from global_vars import global_vars
import config

# Models a journal, which is created on init, or retrieved on init
class notion_journal:
	
	config = config.config('config_notion')
	
	def get_notion_headers(self):
		return {'Authorization': 'Bearer %s' % self.config.get_item('notion','ACCESS_KEY'), 'Content-Type':'application/json','Notion-Version':'2022-02-22'}
	
	# creates a journal if it doesn't exist
	def __init__(self,_config_parser):
		today = datetime.datetime.now().strftime("%Y-%m-%d")
		
		payload = {"filter": { "or" : [ { "property" : "title", "title" : { "starts_with" : today } }, { "property" : "Date", "date" : { "equals" : today } } ] } }
		
		request_url = 'https://api.notion.com/v1/databases/%s/query' % self.config.get_item('notion','INBOX_JOURNAL_KEY')
		
		response = requests.post(request_url, json = payload,headers=self.get_notion_headers())
		
		global journal_id
		
		# Controleer of jounal is aangemaakt
		if len(response.json()['results']) > 0:
			journal_id = response.json()['results'][0]['id'] # journal bestaat, geef ID terug
		else:
			journal_title = '%s %s' % (today,global_vars.DAYS_OF_WEEK[datetime.datetime.now().weekday()]) # hij bestaat niet, maak hem aan
			journal_content = {'parent':{'database_id':config.get_item('notion','INBOX_JOURNAL_KEY')}, 'properties':{'title':{'title':[{"text":{"content":journal_title}}]},'Date':{'date':{'start':today}}}}
			response = requests.post('https://api.notion.com/v1/pages', json=journal_content,headers=self.get_notion_headers()) # Deze regel maakt de journal aan
			journal_id = response.json()['id']

	# Get the goal, always retrieves the journal because it could be updated.
	def get_goal(self):
		request_url = 'https://api.notion.com/v1/pages/%s' % journal_id
		response = requests.get(request_url ,headers=self.get_notion_headers())
		if len(response.json()['properties']['Doel (Commander\'s Intent)']['rich_text']) > 0:
			return response.json()['properties']['Doel (Commander\'s Intent)']['rich_text'][0]['plain_text']
		else:
			return 'no goal defined'
		