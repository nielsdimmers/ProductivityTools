from notion_journal_interface import notion_journal
import datetime

def test_number(_property,_value = 5):
	journal.set_journal_property(_property,_value)
	assert journal.get_journal_property(_property) == _value, "%s not properly set, should be %s" % (_property,_value)

if __name__ == "__main__":
	journal = notion_journal('1987-10-20')
	test_number('LinkedIn connections')
	print("Everything passed, deleting test page")
	journal.delete_journal()
 	
