import imaplib
from config import config
from notion_journal_interface import notion_journal
import email
import global_vars
import log

class mailcheck:

	log = log.log()

	def check_mail(self):
		mail_config = config.config('config_mail')

		# connect to host using SSL
		imap = imaplib.IMAP4_SSL(mail_config.get_item('mail','imap_host'))

		## login to server
		imap.login(mail_config.get_item('mail','imap_user'), mail_config.get_item('mail','imap_pass'))
		imap.select('Inbox')
															 
		tmp, data = imap.search(None, mail_config.get_item("mail","allowed_senders_query"))

		for num in data[0].split():
			tmp, data = imap.fetch(num, '(RFC822)')
			mail_message = email.message_from_bytes(data[0][1])

			body = ''
			if mail_message.is_multipart():
				for part in mail_message.walk():
					# skip any text/plain (txt) attachments
					if part.get_content_type() == 'text/plain' and 'attachment' not in str(part.get('Content-Disposition')):
						body = part.get_payload(decode=True)  # decode
						break
			# not multipart - i.e. plain text, no attachments, keeping fingers crossed
			else:
				body = mail_message.get_payload(decode=True)
	
			micro_journal = ''	
			if mail_message.get_content_charset() != None:
				email_body = body.decode(mail_message.get_content_charset())
			else:
				email_body = body.decode('iso-8859-1') # see changelog of 2023-02-07 in README.md

			if global_vars.MAIL_JOURNAL_BLOCK in email_body:
				micro_journal = email_body.split(global_vars.MAIL_JOURNAL_BLOCK)[1] # There can only be a single microjournal in an e-mail.
			else:
				continue
	
			notion = notion_journal()
			notion.micro_journal(micro_journal)
			result = imap.copy(num,mail_config.get_item('mail','archive_folder'))
			if result[0] == 'OK':
				imap.store(num,'+FLAGS','\\Deleted')
				imap.expunge()
			else:
				self.log.log('WARNING','Could not archive e-mail, e-mail not deleted, error: %s' % result)
		
		imap.close()