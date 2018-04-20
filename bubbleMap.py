def create_bubble_map():
    py.tools.set_credentials_file(username='matt.thomas1202', api_key='XrnxEweYN4ikKVUjdKTA')
    conn = sqlite3.connect('applications.sqlite')
    c = conn.cursor()

    df = pd.read_sql_query('''select city, lat, long, count(*) as count from application, company, location  where company.cid = application.cid and company.lid = location.lid group by location.lid order by count desc''', conn)
   #Set the limits dynamically each time code is run
    c.execute('''select city, count(*) as count from application, company, location where company.cid = application.cid and company.lid = location.lid group by location.lid order by count desc''')
    cities = c.fetchall()
    #initialize limits at zero
    lim1 = lim2 = lim3 =lim4 = lim5 = 0
    #find out how many cities are in each group
    for city in cities:
        if city[1] >= 20:
            lim1 += 1
        elif city[1] >= 15:
            lim2 += 1
        elif city[1] >= 10:
            lim3 += 1
        elif city[1] >= 3:
            lim4 += 1
        else:
            lim5 += 1
    #every limit is based off those that are before it
    lim2 += lim1
    lim3 += lim2
    lim4 += lim3
    lim5 += lim4

    apps = [(20,200),(15,19),(14,10),(3,9),(1,2)]
    limits = [(0,lim1),(lim1,lim2),(lim2,lim3),(lim3,lim4), (lim4,lim5)]
    colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","lightgrey"]
    cities = []


    for i in range(len(limits)):
        lim = limits[i]
        app = apps[i]
        df_sub = df[lim[0]:lim[1]]
        city_text = []
        count = []
        for x in range(len(df_sub)):
            city_text.append(df_sub.loc[df_sub.index[x], 'city'])
            count.append(df_sub.loc[df_sub.index[x], 'count'])
        city_count = list(zip(city_text,count))
        #print(city_count)

        city = dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = df_sub['long'],
            lat = df_sub['lat'],
            sizemode = 'diameter',
            marker = dict(
                size = df_sub['count'],
                color = colors[i],
                line = dict(width = 2,color = 'black')
            ),
            name = '{0} - {1}'.format(app[0],app[1]),
            text = city_count)
        cities.append(city)

    layout = dict(
        title='Application Cities<br>(Click legend to toggle traces)',
        showlegend=True,
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showland=True,
            landcolor='rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        ),
    )

    fig = dict(data=cities, layout=layout)
    url = py.plotly.plot(fig, validate=False, filename='d3-bubble-map-populations')
