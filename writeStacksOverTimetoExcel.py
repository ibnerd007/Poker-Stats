import pandas as pd

from calcAvgSessionStacks import *
from stacksOverTimeLineChart import *
from calcNetStacks import *

def writeStacksOverTimetoExcel(sessionStacks, playerNames, stackChangeInfo, playerIDs, handTypeDesired, dateFormat):

	if handTypeDesired != 'combined':
		# print("Stacks over time not filled, handTypeDesired != 'combined'\n")
		return

	rawDataPath = r'Outputs\stacks_over_time_raw.xlsx'
	avgDataPath = r'Outputs\stacks_over_time_avg.xlsx'

	rawNetDataPath = r'Outputs\net_over_time_raw.xlsx'
	avgNetDataPath = r'Outputs\net_over_time_avg.xlsx'

	# print('Printing stacks vs time raw & avg data & charts to <{}> and <{}>...'.format(rawDataPath, avgDataPath))

	# Calculate moving average of stack and net data -----------------------------------------------------

	avgStacks = calcAvgSessionStacks(sessionStacks, 10)
	net = calcNetStacks(sessionStacks, stackChangeInfo, playerIDs)
	avgNet = calcAvgSessionStacks(net, 10)

	# Create dataframes for each of the four 2D lists (raw, avg, rawNet, avgNet) -------------------------

	rawDf = pd.DataFrame(sessionStacks, columns=playerNames)
	avgDf = pd.DataFrame(avgStacks, columns=playerNames)

	rawNetDf = pd.DataFrame(net, columns=playerNames)
	avgNetDf = pd.DataFrame(avgNet, columns=playerNames)

	# Send all four dataframes to Excel ------------------------------------------------------------------

	rawDf.to_excel(rawDataPath, sheet_name='data', index_label='Hand')
	avgDf.to_excel(avgDataPath, sheet_name='data', index_label='Hand')

	rawNetDf.to_excel(rawNetDataPath, sheet_name='data', index_label='Hand')
	avgNetDf.to_excel(avgNetDataPath, sheet_name='data', index_label='Hand')

	# Create line charts in Excel for the data -----------------------------------------------------------

	stacksOverTimeLineChart(rawDataPath, playerNames, sessionStacks, dateFormat)
	stacksOverTimeLineChart(avgDataPath, playerNames, avgStacks, dateFormat, 10)

	stacksOverTimeLineChart(rawNetDataPath, playerNames, net, dateFormat)
	stacksOverTimeLineChart(avgNetDataPath, playerNames, avgNet, dateFormat, 10)

