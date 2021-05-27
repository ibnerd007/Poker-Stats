import openpyxl
from openpyxl.chart import (
    LineChart,
    Reference
)

def stacksOverTimeLineChart(path, playerNames, stacks, n=None):
	# Creates and styles line chart for stacks over time

	wb_path = path

	wb = openpyxl.load_workbook(wb_path)
	ws = wb['data'] # access sheet


	c1 = LineChart()
	if 'avg' in path:
		c1.title = 'Stacks vs time this session: {}-hand moving averages'.format(n)
	else:
		c1.title = 'Stacks vs time for this session'

	c1.style = 2
	c1.x_axis.title = 'Hand'

	data = Reference(ws, min_col=2, min_row=1, max_col=len(playerNames)+1, max_row=len(stacks)+1)
	c1.add_data(data, titles_from_data=True)

	ws.add_chart(c1, 'J2')

	wb.save(wb_path)
