def writeStacksOverTimetoExcel(sessionStacks, a):

	stacksVsTimePath = r'Outputs\stacks over time.xlsx'
	print('Printing stacks vs time data & chart to <{}>'.format(stacksVsTimePath))

	df = pd.DataFrame(sessionStacks, columns=a)
	# df.to_excel(r'Outputs\stacks over time.xlsx', sheet_name='rawData', index_label='Hand')
	df.to_excel(stacksVsTimePath, sheet_name='avgData', index_label='Hand')

	stacksOverTimeLineChart(a, sessionStacks)
