import matplotlib.pyplot as plt
from notion_journal_interface import notion_journal
from global_vars import global_vars
import datetime
from config import config
from io import BytesIO

# This is a class to generate a report
class report:
	
	def __init__(self):
		self.config = config.config()
	
	def plot_graph(self,x_values, y_values, title="Graph", x_label="X-axis", y_label="Y-axis"):
		# Plot the graph
		plt.plot(x_values, y_values, 'ro-')

		# Set the title and labels
		plt.title(title)
		plt.xlabel(x_label)
		plt.ylabel(y_label)
		plt.xticks(x_values)
		
		# Add labels next to the plotted dots
		for x, y in zip(x_values, y_values):
			label = f'({y})'
			plt.text(x, y, label, ha='right', va='bottom', color='green')

		# Show the grid
		plt.grid(True)
		
		# Save the plot to a BytesIO object
		buffer = BytesIO()
		plt.savefig(buffer, format='png')
		buffer.seek(0)

		# Close the plot to free resources
		plt.close()

		# Return the BytesIO object
		return buffer
			
	def retrieve_weights(self):
		
		y_values = []
		x_values = []
		
		# get the past X weights
		offset = 0 - int(self.config.get_item('report','REPORT_LOOKBACK_LENGTH'))
		
		# NOTE: This part of the code is highly inefficient, better would be to get all journal entries in one go.
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
		graph_image = self.plot_graph(x_values, y_values, title=global_vars.REPORT_GRAPH_TITLE, x_label=global_vars.REPORT_GRAPH_X_LABEL, y_label=global_vars.REPORT_GRAPH_Y_LABEL)
		return graph_image