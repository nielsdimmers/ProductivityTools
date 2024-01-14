import requests
from config import config
import notion_json_builder
import datetime

class data_interface:
	
	def __init__(self):
		self.config = config.config('config_notion')

	# Returns the headers of the notion message
	def get_notion_headers(self):
		return  notion_json_builder.NotionHeaders(self.config.get_item('notion','ACCESS_KEY')).__dict__
	
	# get the data count for today
	def get_data_count(self,date):
		response = requests.post(
		'https://api.notion.com/v1/databases/%s/query' % self.config.get_item('notion','AI_USAGE_DATABASE_KEY'),
		headers=self.get_notion_headers(),
		json=notion_json_builder.NotionCreateDateFilter(date).__dict__
		)
		return len(response.json()['results'])
