import imaplib
import config
from notion_journal_interface import notion_journal

mail_config = config.config('config_mail')

imap_host = mail_config.get_item('mail','imap_host')
imap_user = mail_config.get_item('mail','imap_user')
imap_pass = mail_config.get_item('mail','imap_pass')

ALLOWED_SENDERS = mail_config.get_item("mail","allowed_senders").split(',')

# connect to host using SSL
imap = imaplib.IMAP4_SSL(imap_host)

## login to server
imap.login(imap_user, imap_pass)

imap.select('Inbox')

tmp, data = imap.search(None, 'ALL')

for num in data[0].split():
	tmp, data = imap.fetch(num, '(RFC822)')
	splitMail = data[0][1].decode('utf-8').split('\r\n')
	
	isSenderOK = False
	isReceiverOK = False
	isMicroJournalText = False
	
	micro_journal = ''
	
	msg_uid = ''
	
	for text in splitMail:
		if "X-Mail-from:" in text:
			mail_address = text.split(' ')[1]
			if mail_address in ALLOWED_SENDERS:
				isSenderOK = True
		if text == mail_config.get_item('mail','delivered_to'):
			isReceiverOK = True
		if isMicroJournalText and text != '---MICROJOURNAL---':
			micro_journal += text
		if isMicroJournalText and text == '---MICROJOURNAL---':
			isMicroJournalText = False
			text = ''
		if '---MICROJOURNAL---' in text:
			isMicroJournalText = True
	
	if isSenderOK and isReceiverOK:
 		notion = notion_journal()
 		notion.micro_journal(micro_journal)
 		result = imap.copy(num,mail_config.get_item('mail','archive_folder'))
 		if result[0] == 'OK':
 			imap.store(num,'+FLAGS','\\Deleted')
 			imap.expunge()
 		else:
 			print('Could not archive e-mail, e-mail not deleted, error: %s' % result)
 			
imap.close()