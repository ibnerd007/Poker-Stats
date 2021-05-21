import openpyxl
from openpyxl.chart import (
    LineChart,
    Reference
)

def stacksOverTimeLineChart(a, sessionStacks):
	# Creates and styles line chart for stacks over time

	wb_path = r'Outputs\stacks over time.xlsx'

	wb = openpyxl.load_workbook(wb_path)
	ws = wb['dataHere'] # access sheet


	c1 = LineChart()
	c1.title = 'Stacks over time for this session'
	c1.style = 13
	c1.x_axis.title = 'Hand'

	data = Reference(ws, min_col=2, min_row=1, max_col=len(a)+1, max_row=len(sessionStacks)+1)
	c1.add_data(data, titles_from_data=True)

	ws.add_chart(c1, 'a10')

	wb.save(wb_path)
