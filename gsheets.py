import pygsheets
import numpy as np

class GSheetsService:
    service = None
    spreadsheet = None

    def __init__(self):
        self.service = pygsheets.authorize()

    def create(self, title):
        self.spreadsheet = self.service.create(title)
        print('Access your new spreadsheet "{0}" here: {1}'.format(title, self.spreadsheet.url))

    def write_users(self, credentials):
        # Open Worksheet
        i = 2
        wks = self.spreadsheet.sheet1
        wks.update_value('A1', 'Login')
        wks.update_value('B1', 'Password')
        wks.update_value('C1', 'Taken?')
        wks.cell('A1').set_text_format('bold', True)
        wks.cell('B1').set_text_format('bold', True)
        wks.cell('C1').set_text_format('bold', True)
        for login, password in credentials.items():
            wks.update_value('A{}'.format(i), login)
            wks.update_value('B{}'.format(i), password)
            i+=1