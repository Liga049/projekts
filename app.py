import flask
from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def home():
    nav_links = [
        {"name": "Sākums", "id": "sākums"},
        {"name": "Rezultāti 1", "id": "rezultati-1"},
        {"name": "Rezultāti 2", "id": "rezultati-2"},
    ]
    return render_template('index.html', nav_links=nav_links)

@app.route('/rezultati1')
def rezultati1():
    nav_links = [
        {"name": "Sākums", "id": "sākums"},
        {"name": "Rezultāti 1", "id": "rezultati-1"},
        {"name": "Rezultāti 2", "id": "rezultati-2"},
    ]
    df = pd.read_csv("data/rezultati1.csv")  
    table_html = df.to_html(classes="table table-striped", index=False)

    custom_colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6']

    plt.figure(figsize=(6,6))
    df.groupby('Jūsu vecuma grupa:').size().plot(kind='pie', colors=custom_colors,
                                                 autopct='%1.0f%%', startangle=140,
                                                 wedgeprops={'edgecolor': 'black'})
    plt.title("Vecuma Grupas Sadalījums")

    plt.savefig("static/chart.png")
    plt.close()

    return render_template('rezultati1.html', nav_links=nav_links, table_html=table_html)


@app.route('/rezultati2')
def rezultati2():
    nav_links = [
        {"name": "Sākums", "id": "sākums"},
        {"name": "Rezultāti 1", "id": "rezultati-1"},
        {"name": "Rezultāti 2", "id": "rezultati-2"},
        ]
    df = pd.read_csv("data/doku_hist.csv") 

    df_dokumentalas = df[df['Kāds ir jūsu mīļākais filmu žanrs?'] == 'Dokumentālās'] 

    custom_colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6']

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

    df_dokumentalas["Vecums"] = df_dokumentalas["Jūsu vecuma grupa:"].map(vecuma_mapping)

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
