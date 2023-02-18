import imaplib
from Nconfig import config
from notion_journal_interface import notion_journal
#from email.message import EmailMessage
import email
import base64

mail_config = config.config('config_mail')

# connect to host using SSL
imap = imaplib.IMAP4_SSL(mail_config.get_item('mail','imap_host'))

## login to server
imap.login(mail_config.get_item('mail','imap_user'), mail_config.get_item('mail','imap_pass'))
imap.select('Inbox')
                               
tmp, data = imap.search(None, mail_config.get_item("mail","allowed_senders_query"))

for num in data[0].split():
	tmp, data = imap.fetch(num, '(RFC822)')
	test_mail = email.message_from_bytes(data[0][1])

	body = ''
	
	if test_mail.is_multipart():
		for part in test_mail.walk():
				ctype = part.get_content_type()
				cdispo = str(part.get('Content-Disposition'))

				# skip any text/plain (txt) attachments
				if ctype == 'text/plain' and 'attachment' not in cdispo:
						body = part.get_payload(decode=True)  # decode
						break
	# not multipart - i.e. plain text, no attachments, keeping fingers crossed
	else:
		body = test_mail.get_payload(decode=True)
	
	micro_journal = ''	
	if test_mail.get_content_charset() != None:
		email_body = body.decode(test_mail.get_content_charset())
	else:
		email_body = body.decode('iso-8859-1') # see changelog of 2023-02-07 in README.md

	if '---MICROJOURNAL---' in email_body:
		micro_journal = email_body.split('---MICROJOURNAL---')[1] # There can only be a single microjournal in an e-mail.
	else:
		continue
	
	notion = notion_journal()
	notion.micro_journal(micro_journal)
	result = imap.copy(num,mail_config.get_item('mail','archive_folder'))
	if result[0] == 'OK':
		imap.store(num,'+FLAGS','\\Deleted')
		imap.expunge()
	else:
		print('Could not archive e-mail, e-mail not deleted, error: ')
		print(*result)			
		
imap.close()