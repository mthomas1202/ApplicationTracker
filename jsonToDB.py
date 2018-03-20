import sqlite3
import json
from datetime import datetime
import location_finder as lf


def create_tables(c):
    c.execute( '''CREATE TABLE IF NOT EXISTS application (aID int, position text, cID int, date date, email)''')
    c.execute( '''CREATE TABLE IF NOT EXISTS company (cID int, name text, lID int)''')
    c.execute( '''CREATE TABLE IF NOT EXISTS location (lID int, city text, lat float, long float)''')

def delete_tables(c):
    c.execute('DROP TABLE application')
    c.execute('DROP TABLE company')
    c.execute('DROP TABLE location')


def get_company_values():
    data = json.load(open('applications.json'))
    companies = {}
    i = 1
    for app in data:
        inComp = False
        lID = i
        for value in companies.values():
            if value['name'] == app['company-name']:
                inComp = True
                break

        if inComp:
            continue

        LOCATIONS = json.load(open('locations.json'))
        for location in LOCATIONS.values():
            if app['city'] == location['city']:
                lID = location['lID']


        index = 'c'+ str(i)
        companies[index] = {}
        companies[index]['cID'] = i
        companies[index]['name'] = app['company-name']
        companies[index]['lID'] = lID
        i += 1

    return companies

def add_companies(c):

    companies = get_company_values()
    for company in companies.values():
         cID = str(company['cID'])
         c.execute('SELECT * FROM company WHERE cID = ' + cID)
         result = c.fetchone()
         if not result:
            c.execute('INSERT INTO company VALUES(?,?,?)',[cID,company['name'],company['lID']])
            print(cID,company['name'],company['lID'], 'added to company')

def get_app_data():
    data = json.load(open('applications.json'))
    applications = {}
    i = 1
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
        applications[index]['date'] = datetime.strptime(app['date'], "%m/%d/%Y").date()
        applications[index]['email'] = app['email']
        i += 1

    return applications

def add_apps(c, conn):
    apps = get_app_data()
    i = 1
    for app in apps.values():
        aID = str(i)
        c.execute('SELECT * FROM application WHERE aID = ' + aID)
        result = c.fetchone()
        if not result:
            c.execute('INSERT INTO application VALUES(?,?,?,?,?)', [aID, app['position'], app['cID'], app['date'], app['email']])
            print(aID, app['position'], app['cID'], app['date'], app['email'], 'added to application')
            conn.commit()
        i += 1

def add_locations(conn, c):
    LOCATIONS = json.load(open('locations.json'))
    lID = 1
    for location in LOCATIONS.values():
        c.execute('SELECT * FROM location WHERE lID = "%d" ' %(lID))
        result = c.fetchone()
        if not result:
            c.execute('INSERT INTO location VALUES(?,?,?,?)', [lID, location['city'], location['lat'], location['long']])
            print(lID, location['city'], location['lat'], location['long'], 'added to location')
            conn.commit()
        lID += 1



def update_tables():
    print('Inserting JSON to DB')
    conn = sqlite3.connect('applications.sqlite')
    c = conn.cursor()

    #delete_tables(c)
    create_tables(c)
    lf.update_locations()
    add_locations(conn, c)
    add_companies(c)
    add_apps(c,conn)

    c.close()
    conn.commit()
    conn.close()
    print('JSON inserted to DB')









