
from flask import Flask, render_template, request, Response, url_for
import pandas as pd
import json
import matplotlib
matplotlib.use('Agg')


import plotly.graph_objs as go
from plotly.offline import plot  #Importing all the required libraries and dependencies

app = Flask(__name__)

@app.route('/',methods=['POST', 'GET'])
def index():
    return render_template("mainpage.html")  # routing to the mainpage.html page



@app.route('/queryselect', methods=['POST', 'GET'])
def queryselect():
    import requests
    value = request.form['search']                        #Pulls down required information from form submission
    API = request.form['API']                             # Pulls in the API key typed in by the user
    if API != 0:
        payload = {"keywords": value, "apikey": API}
        searchval = requests.get("https://www.alphavantage.co/query?function=SYMBOL_SEARCH&apikey=*",
                             params=payload)             #Payload alters the load parameters for the pull request
        dict = searchval.json()
        df = pd.DataFrame(dict['bestMatches'])
        #the next line will allow the transfer of clicked URL attribute to be displayed - sent to /company route
        df["1. symbol"] = df["1. symbol"].apply('<a href="/company/{0}">{0}</a>'.format)
        return render_template('mainpage.html', data=df.to_html(escape=False, render_links=True))
    else:
        return render_template("mainpage.html")          #Handles exception with the API key - requires further tests




@app.route('/company/<random>', methods=['GET', 'POST'])
def company(random):
    import requests
    API = request.args.get('API')                        #Pulls in and remembers the API key for the session
    week = {"symbol": random, "apikey": API}
    weeklyval = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=TSCO.LON&apikey=*",
                             params=week)
    dict1 = weeklyval.json()                                        #Created a dictionary of the pull from JSON format
    weekly_df = pd.DataFrame(dict1['Weekly Time Series'])           #pulls down Weekly values for Tachnical Analysis

    month = {"symbol": random, "apikey": API}
    monthlyval = requests.get(
        "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=TSCO.LON&apikey=*",
        params=month)
    dict2 = monthlyval.json()
    monthly_df = pd.DataFrame(dict2['Monthly Time Series'])         #pulls down Monthly values for Tachnical Analysis

    daily = {"symbol": random, "apikey": API}
    dailyval = requests.get(
        "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=300135.SHZ&apikey=*",
        params=daily)
    dict3 = dailyval.json()
    daily_df = pd.DataFrame(dict3)                                  #pulls down Daily values for Tachnical Analysis

    equity = {"symbol": random, "apikey": API}
    equityval = requests.get(
        "https://www.alphavantage.co/query?function=SMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=*",
        params=equity)
    dict4 = equityval.json()
    equity_df = pd.DataFrame(dict4['Technical Analysis: SMA'])     #pulls down equity values for Tachnical Analysis




    #The next line render_template transfers the data grid to the respective HTML page
    return (render_template('creator.html',data = weekly_df.to_html(escape=False, render_links=True),data2 =
                            monthly_df.to_html(escape=False, render_links=True),
                            data3 = daily_df.to_html(escape=False, render_links=True),
                            data4 = equity_df.to_html(escape=False, render_links=True), API = API)) # routing to the creator.html page





if __name__ == "__main__":
    app.run(debug=True)




