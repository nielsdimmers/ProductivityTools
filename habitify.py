import requests 
from config import config
import datetime

class habitify:

	def __init__(self):
		self.config = config.config('config_habitify')
		self.headers = { 'Authorization' : self.config.get_item('habitify','HABITIFY_KEY') }

	def getCurrentValue(self,habitID):
		url = 'https://api.habitify.me/status/-%s?target_date=%sT23%%3A59%%3A33%%2B02%%3A00' % (self.config.get_item('habitify','HABIT_ID'),datetime.datetime.now().strftime("%Y-%m-%d"))

		return requests.get(url,headers=self.headers).json()['data']['progress']['current_value']