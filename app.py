import flask
from flask import Flask, render_template
import pandas as pd

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

app = Flask(__name__)

nav_links = [
    {"name": "Sākums", "id": "index"},
    {"name": "Rezultāti 1", "id": "rezultati1"},
    {"name": "Rezultāti 2", "id": "rezultati2"},
]

@app.route('/')
def index():
    df = pd.read_csv("data/ah.csv")  
    table_html = df.to_html(classes="table table-striped", index=False)

    custom_colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6']

    plt.figure(figsize=(6,6))
    df.groupby('Vecuma grupa').size().plot(kind='pie', colors=custom_colors,
                                                 autopct='%1.0f%%', startangle=140,
                                                 wedgeprops={'edgecolor': 'black'})
    plt.title("Vecuma Grupas Sadalījums")

    plt.savefig("static/chart.png")
    plt.close()

    return render_template('index.html', nav_links=nav_links, table_html=table_html)


@app.route('/rezultati1')
def rezultati1():
    df = pd.read_csv("data/ah.csv")
    table_html = df.to_html(classes="table table-striped", index=False)
    custom_colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6']

    plt.figure(figsize=(8,6))

    df.groupby('Mīļākais filmu žanrs').size().plot(kind='barh', color=custom_colors)

    plt.title("Mīļākais filmu žanrs")
    plt.savefig("static/stab.png")
    plt.close()

    return render_template('rezultati1.html', nav_links=nav_links, table_html=table_html)


@app.route('/rezultati2')
def rezultati2():
    df = pd.read_csv("data/ah.csv") 

    df_dokumentalas = df[df['Mīļākais filmu žanrs'] == 'Dokumentālā'] 

    vecuma_mapping = {
        "<10": 5,
        "10-20": 15,
        "20-30": 25,
        "30-40": 35,
        "40-50": 45,
        "50-60": 55,
        "60-70": 65,
        "70+": 75
    }

    df_dokumentalas["Vecums"] = df_dokumentalas["Vecuma grupa"].map(vecuma_mapping)

    bins = [10, 20, 30, 40, 50, 60, 70, 80]

    plt.figure(figsize=(8, 5))
    plt.hist(df_dokumentalas['Vecums'], bins=bins, color='skyblue', edgecolor='black')

    plt.xlabel("Vecuma grupa")
    plt.ylabel("Cilvēku skaits")
    plt.title("Dokumentālo filmu popularitāte pēc vecuma")
    plt.xticks(bins)
    
    plt.savefig("static/hist.png")
    plt.close()
    return render_template('rezultati2.html', nav_links=nav_links)


if __name__ == '__main__':
    app.run(debug=True)
