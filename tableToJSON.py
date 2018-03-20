import xlrd
import json
from collections import OrderedDict
import datetime


def table_to_json(table):
    #Open excel workbook and select the first sheet
    wb = xlrd.open_workbook(table)
    sh = wb.sheet_by_index(0)

    app_list = []

    #Iterate over rows in sheet and create dictionary of values by row
    for rownum in range(4, sh.nrows):
        apps = OrderedDict()
        row_values = sh.row_values(rownum)
        apps['company-name'] = row_values[0]
        apps['position'] = row_values[1]
        apps['city'] = row_values[2]
        start_date = datetime.datetime.strptime("01/01/1900", "%m/%d/%Y").date()
        in_date = start_date + datetime.timedelta(days=row_values[3]-2)
        in_date = in_date.strftime('%m/%d/%Y')
        apps['date'] = in_date
        apps['email'] = row_values[4]

        #append dictionary to list
        app_list.append(apps)
    #create json data from list
    j = json.dumps(app_list)
    #write json data to 'applications.json'
    with open('applications.json','w') as f:
        f.write(j)

    print('Table converted to JSON')
