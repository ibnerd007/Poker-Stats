import openpyxl

def wipeCurrSessionSheets(handTypeDesired):
	""" Wipes sheets on stats.xlsx that are unused from current session.
	This provides clarity and avoids confusion, so only one date is presented at a time
	on stats.xlsx. """

	wb_path = r'Outputs\stats.xlsx'
	wb = openpyxl.load_workbook(wb_path) # load existing workbook

	sheet = wb['{} Stats-this session'.format(handTypeDesired)]

	wb.remove(sheet)

	wb.save(wb_path)