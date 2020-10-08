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
        wks = self.spreadsheet.sheet1
        data = np.empty((3,len(credentials.items())+1), dtype=object)
        data[0][0]= 'Login'
        data[0][1]= 'Password'
        data[0][2]= 'Taken?'
        i = 0
        for login, password in credentials.items():
            i+=1
            data[i][0]=login
            data[i][1]=password
            data[i][2]=''
        wks.insert_rows(row=0, number=i, values=data.tolist())