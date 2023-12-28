from telegram.ext import Application, Updater, InlineQueryHandler, CommandHandler, filters, MessageHandler
import matplotlib.pyplot as plt
from notion_journal_interface import notion_journal
from global_vars import global_vars
import datetime
from config import config
import asyncio
import os
# start by generating a report

class report:
	
	def __init__(self):
		self.config = config.config()
	
	def plot_graph(self,x_values, y_values, title="Graph", x_label="X-axis", y_label="Y-axis"):
			# Plot the graph
			plt.plot(x_values, y_values, marker='o')

			# Set the title and labels
			plt.title(title)
			plt.xlabel(x_label)
			plt.ylabel(y_label)

			# Show the grid
			plt.grid(True)

			# Show the plot
			plt.savefig(global_vars.REPORT_GRAPH_FILE)

	def retrieve_weights(self):
		
		y_values = []
		x_values = []
		
		# get the past X weights
		offset = 0 - int(self.config.get_item('report','REPORT_LOOKBACK_LENGTH'))
		while offset < 0:
			date = (datetime.datetime.now() + datetime.timedelta(days=offset)).strftime("%Y-%m-%d")
			weight = notion_journal(date).get_journal_property(global_vars.JOURNAL_WEIGHT_KEY)
			if isinstance(weight, (int, float, complex)):
				y_values.append(weight)
				x_values.append(abs(offset))
			offset += 1
		return [y_values,x_values]


	def send_graph(self):
		# Customize the title and labels as needed
		[y_values,x_values] = self.retrieve_weights()
# 		print('x values are %s and y values are %s' % (x_values,y_values))
		self.plot_graph(x_values, y_values, title=global_vars.REPORT_GRAPH_TITLE, x_label=global_vars.REPORT_GRAPH_X_LABEL, y_label=global_vars.REPORT_GRAPH_Y_LABEL)

		application = Application.builder().token(self.config.get_item('telegram','TELEGRAM_API_TOKEN')).build()
		asyncio.get_event_loop().run_until_complete(application.bot.send_photo(chat_id=self.config.get_item('telegram','TELEGRAM_CHAT_ID'),photo=open(global_vars.REPORT_GRAPH_FILE, 'rb')))
		
		os.remove(global_vars.REPORT_GRAPH_FILE)