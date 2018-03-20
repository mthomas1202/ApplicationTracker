import json
import pandas as pd
import plotly as py
import plotly.graph_objs as go
import sqlite3


def create_line_graph():
    py.tools.set_credentials_file(username='matt.thomas1202', api_key='API_KEY')
    conn = sqlite3.connect('applications.sqlite')
    c = conn.cursor()

    df = pd.read_sql_query('''Select date, count(date) from application group by date order by date''', conn)

    data = [
        go.Scatter(
            x = df['date'],
            y = df['count(date)']
        )
    ]

    layout = go.Layout(
        title = 'Applications by Date',
        yaxis = dict(title='Number of Applications'),
        xaxis = dict(title='Date')
    )

    figure = go.Figure(data=data, layout=layout)

    url = py.plotly.plot(figure, filename='applications-by-date')
