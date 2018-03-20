import googlemaps
import json
import sqlite3
from pprint import pprint

API_KEY = "AIzaSyBrdbysy3Pq9GiCux3GAX8-ZvfFAII-ZTg"


def get_cities():
    data = json.load(open('applications.json'))
    cities = {}
    for company in data:
        cities[company['company-name']] = company['city']
    cities['NSA'] = 'Fort Meade, MD'
    return cities


def get_locations():
    gm = googlemaps.Client(key=API_KEY)
    locations = {}

    cities = get_cities()


    i = 1
    for company, city in cities.items():
        inLoc = False
        for value in locations.values():
            if value['city'] == city:
                inLoc = True
                break

        if inLoc:
            continue

        if check_db(city) == True:
            i += 1
            continue

        index = 'l' + str(i)
        locations[index] = {}
        locations[index]['lID']  = i
        locations[index]['city'] = city
        if city == 'USA' or city == 'Various':
            locations[index]['lat'] = None
            locations[index]['long'] = None
        else:
            geocode = gm.geocode(city)[0]
            locations[index]['lat']  = geocode['geometry']['location']['lat']
            locations[index]['long'] = geocode['geometry']['location']['lng']

        i += 1

    return locations


def check_db(city):
    conn = sqlite3.connect('applications.sqlite')
    c = conn.cursor()

    c.execute('''SELECT * from location where city = "{0}"'''.format(city))
    if not c.fetchall():
        c.close()
        conn.close()
        return False

    c.close()
    conn.close()
    return True



def update_locations():
    LOCATIONS = get_locations()

    j = json.dumps(LOCATIONS)

    with open('locations.json','w') as f:
        f.write(j)






