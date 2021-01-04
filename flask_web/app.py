#map and table
from flask import Flask, render_template
app = Flask(__name__)
import pandas as pd
from werkzeug.utils import html
import folium
corona_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/12-29-2020.csv')

def find_top_confirmed():
    corona_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/12-29-2020.csv')
    by_country = corona_df.groupby('Country_Region').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]
    cdf = by_country.nlargest(15, 'Confirmed')[['Confirmed']]
    return cdf

def circle_maker(x):
      folium.Circle(location = [x[0], x[1]],
                radius = float(x[2])*0.5,
                popup = '{}\nConfirmed Cases: {}'.format(x[3], x[2])).add_to(m) 
corona_df[['Lat', 'Long_', 'Confirmed', 'Combined_Key']].dropna(subset = ['Lat', 'Long_']).apply(lambda x: circle_maker(x), axis = 1)

cdf = find_top_confirmed().to_html()

m = folium.Map(location = [39.992, -105.190],
           tiles = 'Stamen toner',
           zoom_start = 8)
html_map = m._repr_html_()


@app.route('/')
def home():
    return render_template('home.html', table = cdf, c_map = html_map)


if __name__=='__main__':
    app.run(debug=True)