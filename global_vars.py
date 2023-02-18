class global_vars:

	USER_NOT_ALLOWED_ERROR = 'User name %s (id:%s) has no permission to send messages to this bot.'

	DATETIME_WEEK_NUMBER = 'The current week number is %s.'
	
	NOTION_CHILDREN_URL = 'https://api.notion.com/v1/blocks/%s/children'
	
	NOTION_DATABASE_QUERY_URL = 'https://api.notion.com/v1/databases/%s/query'
	
	NOTION_DATABASE_GET_URL = 'https://api.notion.com/v1/databases/%s'
	
	NOTION_PAGE_CREATE_URL = 'https://api.notion.com/v1/pages'
	
	NOTION_PROPERTY_GET_URL = 'https://api.notion.com/v1/pages/%s/properties/%s'
	
	NOTION_JOURNAL_OK_MSG = 'Micro journal with length %s characters and %s words added.\n'
	
	NOTION_JOURNAL_NOK_MSG = 'Error response code %s. Full json follows: \n%s\n'
	
	HTTP_OK_CODE = 200
	
	NOTION_JOURNAL_MULTIPART_ENTRY = 'Multi part journal entry follows:'
	
	NOTION_PAGE_URL = 'https://api.notion.com/v1/pages/%s'
	
	DAYS_OF_WEEK = ['maandag','dinsdag','woensdag','donderdag','vrijdag','zaterdag','zondag']
	
	TELEGRAM_SEND_ERROR = 'Error sending message to Telegram: \n%s\n\n'
	
	REBOOT_MESSAGE = 'Hallo daar ben ik weer!'
	
	NOTION_JOURNAL_JSON = '{"children":[{"object":"block", "type":"paragraph", "paragraph":{"rich_text":[{"type":"text","text": {"content": "%s"} }] }}]}'
	
	NOTION_NUMBER_PROPERTY_JSON = '{"properties": { "%s" : {"number":%s}}}'
	
	NOTION_RICHTEXT_PROPERTY_JSON = '{"properties": { "%s" : {"rich_text": [{"text": {"content" : "%s"}}]}}}'
	
	NOTION_PROPERTY_JSON = {'rich_text' : NOTION_RICHTEXT_PROPERTY_JSON,'number' : NOTION_NUMBER_PROPERTY_JSON}
	
	NOTION_RETRIEVE_JOURNAL_JSON = '{"filter": { "or" : [ { "property" : "title", "title" : { "starts_with" : "%s" } }, { "property" : "Datum", "date" : { "equals" : "%s" } } ] } }'
	
	NOTION_TASKLIST_QUERY_JSON = '{"filter": { "and": [{"property": "Status", "status" : { "does_not_equal": "Done 🙌" } },  { "property": "Status", "status" : { "does_not_equal": "Dropped 🔥" } }, {  "or": [ { "property":"Due date", "date" :{ "on_or_before":"%s" } }, { "property":"Action date", "date" : { "on_or_before":"%s" } } ] } ] } }'
	
	
	## LOGGING
	LOG_LENGTH_MESSAGE = 'The logfile %s is %s lines long.'
	
	# the telegram URL to send a message to myself
	TELEGRAM_MSG_URL = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s&parse_mode=Markdown"
	
	SCRIPT_USAGE = "Usage:\n python3 ./script.py <command>\n - daily for daily data\n - logcount count of log length\n - test run automated tests"