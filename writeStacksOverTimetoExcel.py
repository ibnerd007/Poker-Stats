from calcAvgSessionStacks import *
from stacksOverTimeLineChart import *
import pandas as pd

def writeStacksOverTimetoExcel(sessionStacks, playerNames):

	rawDataPath = r'Outputs\stacks_over_time_raw.xlsx'
	avgDataPath = r'Outputs\stacks_over_time_avg.xlsx'

	# print('Printing stacks vs time raw & avg data & charts to <{}> and <{}>...'.format(rawDataPath, avgDataPath))

	avgStacks = calcAvgSessionStacks(sessionStacks, 10)

	rawDf = pd.DataFrame(sessionStacks, columns=playerNames)
	avgDf = pd.DataFrame(avgStacks, columns=playerNames)
	
	rawDf.to_excel(rawDataPath, sheet_name='data', index_label='Hand')
	avgDf.to_excel(avgDataPath, sheet_name='data', index_label='Hand')

	stacksOverTimeLineChart(rawDataPath, playerNames, sessionStacks)
	stacksOverTimeLineChart(avgDataPath, playerNames, avgStacks, 10)

