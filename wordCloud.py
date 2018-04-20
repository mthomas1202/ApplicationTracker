import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import sqlite3
from collections import Counter

def generate_wordcloud():
    conn = sqlite3.connect('applications.sqlite')
    c = conn.cursor()

    df = pd.read_sql_query('''select position from application''', conn)

    string = ""

    for index, row in df.iterrows():
        string += row['position'] + " "

    wordCounts = Counter(string.split())

    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies = wordCounts)
    plt.figure()
    plt.imshow(wordcloud, interpolation = "bilinear")
    plt.axis("off")
    plt.show()
