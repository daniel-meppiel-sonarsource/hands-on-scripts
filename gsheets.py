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

    def write_users(self, users_list):
        # Open Worksheet
        wks = self.spreadsheet.sheet1
        data = np.empty((len(users_list)+1, 4), dtype=object)
        data[0][0]= 'Login'
        data[0][1]= 'Password'
        data[0][2]= 'Token'
        data[0][3]= 'Used By'
        i = 0
        for user in users_list:
            i+=1
            data[i][0]=user.login
            data[i][1]=user.password
            data[i][2]=user.token
            data[i][3]=''
        wks.insert_rows(row=0, number=i, values=data.tolist())
        wks.adjust_column_width(3,3)