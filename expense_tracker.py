# import os
# dir_path = os.path.dirname(os.path.realpath(__file__))
# import sys
# sys.path.append(os.path.join(dir_path, 'lib'))

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def next_available_row(worksheet):
    str_list = filter(None, worksheet.col_values(1))  # fastest
    return str(len(str_list)+1)

def add_entry(expense_category, description, price, invoices=""):
    sheet_link = json.load(open('sheets.json'))[expense_category]
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    # sheet = client.open("house expenses").sheet1
    worksheet = client.open_by_url(sheet_link).sheet1
    # Extract and print all of the values
    next_row = next_available_row(worksheet)
    # Select a range
    cell_list = worksheet.range('A{}:C{}'.format(next_row, next_row))
    cell_list[0].value = description
    cell_list[1].value = invoices
    cell_list[2].value = price
    worksheet.update_cells(cell_list)