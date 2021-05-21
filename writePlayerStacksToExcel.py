import pandas as pd

def writePlayerStacksToExcel(stacks):

	wb_path = r'Outputs\stats.xlsx'
	sheet = 'Stacks vs time'

	df = pd.DataFrame()

	df.append(stacks)
	



