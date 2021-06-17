import openpyxl
from openpyxl.chart import (
    LineChart,
    Reference
)

def stacksOverTimeLineChart(path, playerNames, stacks, dateFormat, n=None):
	# Creates and styles line chart for stacks over time

	wb = openpyxl.load_workbook(path)
	ws = wb['data'] # access sheet

	if 'net' in path: name = 'Net vs time'
	else:             name = 'Stacks vs time'


	c1 = LineChart()
	if 'avg' in path:
		c1.title = '{} this session ({}): {}-hand moving averages'.format(name, dateFormat, n)
	else:
		c1.title = '{} for this session ({})'.format(name, dateFormat)

	c1.style = 2
	c1.x_axis.title = 'Hand'

	c1.height = 18
	c1.width = 32

	data = Reference(ws, min_col=2, min_row=1, max_col=len(playerNames)+1, max_row=len(stacks)+1)
	c1.add_data(data, titles_from_data=True)

	ws.add_chart(c1, 'A1')

	wb.save(path)
