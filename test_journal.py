from Nconfig.config import config
from notion_journal_interface import notion_journal
from global_vars import global_vars

import datetime


global_vars = global_vars()
config = config('config_notion')
notion_journal = notion_journal(config.get_item('notion','TEST_DATE'))

def test_number(_property,_value = 5):
	notion_journal.set_journal_property(_property,_value)
	assert notion_journal.get_journal_property(_property) == _value, "%s not properly set, should be %s" % (_property,_value)

# Gives wrong result when used with Micro Journals containing newlines or longer than the notion limit.
def test_micro_journal(_text):
	assert notion_journal.micro_journal(_text) == global_vars.NOTION_JOURNAL_OK_MSG % (len(_text),len(_text.split())), "Micro journal not properly set."
	
def test_count_words(_words):
	assert notion_journal.count_words() == _words, "Micro journal count_words not correct. Actual value is %s" % notion_journal.count_words()

if __name__ == "__main__":
	micro_journal_text = 'Dit is een kort microjournal testbericht'
	test_number('LinkedIn connections')
	test_micro_journal(micro_journal_text)
	test_count_words(len(micro_journal_text.split()) + 1)
	print("Everything passed, deleting test page")
	notion_journal.delete_journal()
 	
