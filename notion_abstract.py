from config import config
import notion_json_builder
import requests
from global_vars import global_vars

# models abstract class for notion interfaces
class notion_abstract:

	def __init__(self): # see update 63 in readme why this is needed.
		self.config = config.config('config_notion')
	
	def get_config(self,_item):
		return self.config.get_item('notion',_item)

	# Returns the headers of the notion message
	def get_notion_headers(self):
		return  notion_json_builder.NotionHeaders(self.config.get_item('notion','ACCESS_KEY')).__dict__

	def post_notion(self,_type_request,_id,_json):
		if _type_request == 'database':
			return requests.post('https://api.notion.com/v1/databases/%s/query' % _id,json=_json,headers=self.get_notion_headers())
		if _type_request == 'page':
			return requests.post('https://api.notion.com/v1/pages', json=_json,headers=self.get_notion_headers())

	def patch_notion(self,_type_request,_id,_json):
		if _type_request == 'children':
			return requests.patch(global_vars.NOTION_CHILDREN_URL % _id,json=_json,headers=self.get_notion_headers())
		if _type_request == 'page':
			return requests.patch(global_vars.NOTION_PAGE_URL % _id,json=_json, headers = self.get_notion_headers())
			
	def get_notion(self,_type_request,_key):
		if _type_request == 'database':
			return requests.get(global_vars.NOTION_DATABASE_GET_URL % _key,headers=self.get_notion_headers())
		elif _type_request == 'page':
			return requests.get(global_vars.NOTION_PAGE_URL % _key,headers=self.get_notion_headers())
		elif _type_request == 'children':
			return requests.get(global_vars.NOTION_CHILDREN_URL  % _key, headers=self.get_notion_headers()).json()['results']