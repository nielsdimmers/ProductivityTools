import configparser
import sys
import requests

# Parse the notion vars from the config file
configParser = configparser.RawConfigParser()
configParser.read(r'.config')

# Parse the authentication
auth = 'Bearer %s' % configParser.get('notion','ACCESS_KEY')

# JSON Headers
headers = {'Authorization': auth, 'Content-Type':'application/json','Notion-Version':'2021-08-16'}

# JSON body
dictionary = {'parent':{'database_id':configParser.get('notion','INBOX_DATABASE_KEY')}, 'properties':{'title':{'title':[{"text":{"content":sys.argv[1]}}]}}}

# The actual call
response = requests.post('https://api.notion.com/v1/pages', json=dictionary,headers=headers)

# Print the response
print(response.text)

# and the status code last
print('status code: %s-%s'%(response.status_code,response.reason))
