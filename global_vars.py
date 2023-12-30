class global_vars:

	USER_NOT_ALLOWED_ERROR = 'User name %s (id:%s) has no permission to send messages to this bot.'
	
	TELEGRAM_SEND_ERROR = 'Error sending message to Telegram: \n%s\n\nError message: %s'

	REBOOT_MESSAGE = 'Hi I\'m back again!'

	DATETIME_WEEK_NUMBER = 'The current week number is %s.'

	# the telegram URL to send a message to myself
	TELEGRAM_MSG_URL = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&parse_mode=Markdown"
	
	NOTION_CHILDREN_URL = 'https://api.notion.com/v1/blocks/%s/children'
	
	NOTION_DATABASE_QUERY_URL = 'https://api.notion.com/v1/databases/%s/query'
	
	NOTION_DATABASE_GET_URL = 'https://api.notion.com/v1/databases/%s'
	
	NOTION_PAGE_CREATE_URL = 'https://api.notion.com/v1/pages'
	
	NOTION_PROPERTY_GET_URL = 'https://api.notion.com/v1/pages/%s/properties/%s'
	
	NOTION_JOURNAL_LENGTH_MSG = 'With %s words you are at %s%% of your words goal of %s.'
	
	NOTION_JOURNAL_OK_MSG = 'Added a new micro journal to the journal dated %s, journal has length %s characters and %s words.\n'
	
	NOTION_JOURNAL_NOK_MSG = 'Error response code %s. Full json follows: \n%s\n'
	
	HTTP_OK_CODE = 200
	
	NOTION_JOURNAL_MULTIPART_ENTRY = 'Multi part journal entry follows:'
	
	NOTION_PAGE_URL = 'https://api.notion.com/v1/pages/%s'
	
	DAYS_OF_WEEK = ['maandag','dinsdag','woensdag','donderdag','vrijdag','zaterdag','zondag']
	
	NOTION_JOURNAL_JSON = '{"children":[{"object":"block", "type":"paragraph", "paragraph":{"rich_text":[{"type":"text","text": {"content": "%s"} }] }}]}'
	
	NOTION_NUMBER_PROPERTY_JSON = '{"properties": { "%s" : {"number":%s}}}'
	
	NOTION_RICHTEXT_PROPERTY_JSON = '{"properties": { "%s" : {"rich_text": [{"text": {"content" : "%s"}}]}}}'
	
	NOTION_PROPERTY_JSON = {'rich_text' : NOTION_RICHTEXT_PROPERTY_JSON,'number' : NOTION_NUMBER_PROPERTY_JSON}
	
	NOTION_RETRIEVE_JOURNAL_JSON = '{"filter": { "or" : [ { "property" : "title", "title" : { "starts_with" : "%s" } }, { "property" : "Date", "date" : { "equals" : "%s" } } ] } }'
	
	NOTION_TASKLIST_QUERY_JSON = '{"filter": { "and": [{"property": "Status", "status" : { "does_not_equal": "Done 🙌" } },  { "property": "Status", "status" : { "does_not_equal": "Dropped 🔥" } }, {  "or": [ { "property":"Due date", "date" :{ "on_or_before":"%s" } }, { "property":"Action date", "date" : { "on_or_before":"%s" } } ] } ] } }'
	
	JOURNAL_DATE_KEY = 'Date'
	
	JOURNAL_LENGTH_KEY = 'Journal length'
	
	JOURNAL_ONE_PERCENT_KEY = '1% better'
	
	JOURNAL_GOAL_KEY = 'Goal'
	
	JOURNAL_WEIGHT_KEY = 'Weight (Kg)'
	
	JOURNAL_FUN_KEY = 'Fun for today'
	
	## LOGGING
	LOG_LENGTH_MESSAGE = 'The logfile %s is %s lines long.'
		
	SCRIPT_USAGE = "Usage:\n python3 ./script.py <command>\n - daily for daily data\n - logcount count of log length\n - test run automated tests\n - legal for copyright information\n - listener to start the listener\n - mailcheck to check the mail\n - words to send a wordcount message."
	
	LEGAL_NOTICE = "This program is licensed under the GNU General Public License version 3.0 (2007). For the full text, see [the license file on github](https://github.com/nielsdimmers/ProductivityTools/blob/main/LICENSE). The code to my bot can be found on [github](https://github.com/nielsdimmers/ProductivityTools)."
	
	MAIL_JOURNAL_BLOCK = '---MICROJOURNAL---'
	
	REPORT_GRAPH_FILE = 'tmp/plot.jpg'
	
	REPORT_GRAPH_TITLE = 'Weight histograph'
	
	REPORT_GRAPH_Y_LABEL = 'Weight (Kg)'
	
	REPORT_GRAPH_X_LABEL = 'Days ago'
	
	REPORT_IMAGE_NOT_FOUND_ERR = 'Error: graph image not found'