def writeStacksOverTimetoExcel(sessionStacks, playerNames):

	rawPath = r'Outputs\stacks_over_time_raw.xlsx'
	avgPath = r'Outputs\stacks_over_time_avg.xlsx'

	print('Printing stacks vs time raw & avg data & charts to \
		   <{}> and <{}>...'.format(rawPath, avgPath))

	avgSessionStacks = calcAvgSessionStacks(sessionStacks)

	rawDf = pd.DataFrame(sessionStacks, columns=playerNames)
	avgDf = pd.DataFrame(avgSessionStacks, columns=playerNames)
	
	df.to_excel(rawPath, sheet_name='rawData', index_label='Hand')
	df.to_excel(avgPath, sheet_name='avgData', index_label='Hand')

	stacksOverTimeLineChart(playerNames, sessionStacks)
