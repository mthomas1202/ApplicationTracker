import sqlite3
import json
from datetime import datetime
import location_finder as lf

#creates tables (application, company, location) if they do not exist
def create_tables(c):
    c.execute( '''CREATE TABLE IF NOT EXISTS application (aID int, position text, cID int, date date, email text, status text)''')
    c.execute( '''CREATE TABLE IF NOT EXISTS company (cID int, name text, lID int)''')
    c.execute( '''CREATE TABLE IF NOT EXISTS location (lID int, city text, lat float, long float)''')

#deletes tables if user needs to reinsert data from scratch
def delete_tables(c):
    c.execute('DROP TABLE application')
    c.execute('DROP TABLE company')
    c.execute('DROP TABLE location')

#gather necessary data to store in company table
def get_company_values():
    data = json.load(open('applications.json'))
    companies = {}
    i = 1
    for app in data:
        inComp = False #flag to make sure there are no duplicates
        lID = i
        for value in companies.values():
            if value['name'] == app['company-name']: #goes through dictionary to check if value already present
                inComp = True
                break

        #if value already present, go on to next entry
        if inComp:
            continue

        #make sure that lid in both location and company tables are equal
        LOCATIONS = json.load(open('locations.json'))
        for location in LOCATIONS.values():
            if app['city'] == location['city']:
                lID = location['lID']

        #insert values into companies dictionary
        index = 'c'+ str(i)
        companies[index] = {}
        companies[index]['cID'] = i
        companies[index]['name'] = app['company-name']
        companies[index]['lID'] = lID
        i += 1

    return companies


#insert company values into company table
def add_companies(c):

    insertedCompany = False #flag to see if company is already present in table
    companies = get_company_values() #get company data to insert
    for company in companies.values():
         cID = str(company['cID']) #check if value is already in table
         c.execute('SELECT * FROM company WHERE cID = ' + cID)
         result = c.fetchone()
         if not result: #if not insert values
            c.execute('INSERT INTO company VALUES(?,?,?)',[cID,company['name'],company['lID']])
            print(cID,company['name'],company['lID'], 'added to company') #display what was inserted into table
            insertedCompany = True

    return insertedCompany

#get application data to insert into table
def get_app_data():
    data = json.load(open('applications.json')) #read data from json
    applications = {}
    i = 1
    #get company info so that the cid in application and company are equal
    companies = get_company_values()
    for app in data:
        cID = i
        for value in companies.values():
            if value['name'] == app['company-name']:
                cID = value['cID']
                break


        index = 'a' + str(i)
        applications[index] = {}
        applications[index]['position'] = app['position']
        applications[index]['cID'] = cID
        applications[index]['date'] = datetime.strptime(app['date'], "%m/%d/%Y").date() #convert date into datetime object
        #in case of deletion of table, make sure all old applications are automatically set to no
        if applications[index]['date'] < datetime(2018,1,1).date():
            applications[index]['status'] = "No"
        else:
            applications[index]['status'] = None #otherwise we do not know that status
        applications[index]['email'] = app['email']

        i += 1

    return applications

#insert app values into table
def add_apps(c, conn):
    insertedApps = False #flag to see if values are inserted into table
    apps = get_app_data() #gather data to insert
    i = 1
    for app in apps.values():
        aID = str(i) #check if value is already in table
        c.execute('SELECT * FROM application WHERE aID = ' + aID)
        result = c.fetchone()
        if not result: # if not, insert values
            c.execute('INSERT INTO application VALUES(?,?,?,?,?,?)',[aID, app['position'], app['cID'], app['date'], app['email'], app['status']])
            print(aID, app['position'], app['cID'], app['date'], app['email'], app['status'], 'added to application')
            conn.commit()
            insertedApps = True #value has been inserted so flag set to true
        i += 1

    return insertedApps

#insert location values into table
def add_locations(conn, c):
    insertedLocs = False #flag to see if values have been inserted
    LOCATIONS = json.load(open('locations.json')) #gather data to enter
    for location in LOCATIONS.values():#check if value already in table
        c.execute('SELECT * FROM location WHERE lID = '+ str(location['lID']))
        result = c.fetchone()
        if not result:#if not, insert values
            c.execute('INSERT INTO location VALUES(?,?,?,?)', [location['lID'], location['city'], location['lat'], location['long']])
            print(location['lID'], location['city'], location['lat'], location['long'], 'added to location')
            conn.commit()
            insertedLocs = True #set flag to true

    return insertedLocs


#method called by main.py to update table
def update_tables():
    conn = sqlite3.connect('applications.sqlite') #connect to database
    c = conn.cursor()


    #insert any values that need to be inserted
    create_tables(c)
    lf.update_locations()
    loc = add_locations(conn, c)
    comp = add_companies(c)
    app = add_apps(c,conn)

    #if no values inserted into any table, database up to date
    if not (loc or comp or app):
        print("Database up to date")

    c.close()
    conn.commit()
    conn.close()









