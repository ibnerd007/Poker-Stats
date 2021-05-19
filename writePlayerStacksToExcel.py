import openpyxl

def writePlayerStacksToExcel(stacks):
	
	wb_path = r'Outputs\stats.xlsx'

	wb = openpyxl.load_workbook(wb_path) # load existing workbook

	sheet = wb['Stacks vs time'] # access sheet

	sheet.append(stacks)

	wb.save(wb_path)


