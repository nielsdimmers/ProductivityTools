from global_vars import global_vars

# Headers of notion
class NotionHeaders:
	def __init__(self, access_key):
		self.Authorization = f'Bearer {access_key}'
		self.accept = 'application/json'
		setattr(self, 'Notion-Version', '2022-06-28')
		
class NotionChildren:
	def __init__(self,content):
		self.children = []
		for paragraph in content:
			self.children.append(NotionChildArray(paragraph).__dict__)

class NotionChildArray:
	def __init__(self,content):
		setattr(self, 'object', 'block')
		setattr(self, 'type', 'paragraph')
		setattr(self, 'paragraph', NotionParagraph(content).__dict__)

class NotionParagraph:
	def __init__(self,content):
		setattr(self, 'rich_text', [NotionRichText(content).__dict__])

class NotionRichText:
	def __init__(self,content):
		setattr(self, 'type','text')
		setattr(self, 'text', NotionTextblock(content).__dict__)

class NotionTextblock:
	def __init__(self,content):
		self.content = content
		
class NotionPage:
	def __init__(self,database_id,page_title,journal_date=None):
		self.parent = NotionParent(database_id).__dict__
		self.properties = NotionPageProperties(page_title,journal_date).__dict__
		
class NotionParent:
	def __init__(self,database_id):
		self.database_id = database_id
		
class NotionPageProperties:
	def __init__(self,page_title,journal_date=None):
		setattr(self, 'title', NotionTitleArray(page_title).__dict__)
		if journal_date != None:
			setattr(self, global_vars.JOURNAL_DATE_KEY, NotionDateVar(journal_date).__dict__)
		
class NotionDateVar:
	def __init__(self,date):
		setattr(self,'date',NotionStartDateVar(date).__dict__)
		
class NotionStartDateVar:
	def __init__(self,date):
		setattr(self,'start',date)
		
class NotionTitleArray:
	def __init__(self,content):
		titles = []
		for line in content:
			titles.append(NotionTitleText(line).__dict__)
		setattr(self, 'title', titles)
	
class NotionTitleText:
	def __init__(self,content):
		setattr(self, 'text', NotionTextblock(content).__dict__)

