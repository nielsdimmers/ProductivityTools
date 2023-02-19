from config.config import config
from notion_journal_interface import notion_journal
from global_vars import global_vars

import datetime

class test_journal:
	global_vars = global_vars()
	config = config('config_notion')
	notion_journal = notion_journal(config.get_item('notion','TEST_DATE'))

	def test_number(self,_property,_value = 5):
		self.notion_journal.set_journal_property(_property,_value)
		assert self.notion_journal.get_journal_property(_property) == _value, "%s not properly set, should be %s" % (_property,_value)

	# Gives wrong result when used with Micro Journals containing newlines or longer than the notion limit.
	def test_micro_journal(self,_text):
		assert self.notion_journal.micro_journal(_text) == self.global_vars.NOTION_JOURNAL_OK_MSG % (len(_text),len(_text.split())), "Micro journal not properly set."
	
	def test_count_words(self,_words):
		assert self.notion_journal.count_words() == _words, "Micro journal count_words not correct. Actual value is %s" % self.notion_journal.count_words()

	def test_link(self):
		url = self.notion_journal.get_url()
		assert 'https://' in url, "URL Return does not start with https: %s" % url
		assert self.config.get_item('notion','TEST_DATE') in url, "URL does not contain date: %s" % url

	def run_test(self):
		print("starting test script")
		self.test_link()
		micro_journal_text = 'Dit is een kort microjournal testbericht'
		self.test_number('LinkedIn connections')
		self.test_micro_journal(micro_journal_text)
		self.test_count_words(len(micro_journal_text.split()) + 1)
		print("Everything passed, deleting test page")
		self.notion_journal.delete_journal()
 	
