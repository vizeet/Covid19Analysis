import requests
import json
import pandas as pd
#import plotly.express as px

URL = 'https://api.covid19india.org/v3/data-all.json'

def get_covid_json():
    global URL

    r = requests.get(url = URL)
    jsonobj = r.json()
#    print(json.dumps(jsonobj, indent = 4))

    return jsonobj

def get_test_strike_rate():
    pass

def get_state_list(jsonobj: dict):
    pass

def build_daily_metrics_india(jsonobj: dict):
    daily_metrics = {}
    for date in jsonobj:
        delta = jsonobj[date]['TT']['delta']
        if 'tested' in delta:
            daily_metrics[date] = {}
            daily_metrics[date]['confirmed'] = delta['confirmed']
            daily_metrics[date]['tested'] = delta['tested']
            daily_metrics[date]['test_confirm_rate'] = (delta['confirmed'] * 100) / delta['tested']
    return  daily_metrics

def get_df_metrics_india(jsonobj: dict):
    df = pd.DataFrame.from_dict(jsonobj, orient='index')

    return df

def get_7day_moving_avg(df):
    return df.rolling(window=7).mean().dropna()

def get_date_list(jsonobj: dict):
    for key in jsonobj:
        print(key)

if __name__ == '__main__':
    jsonobj = get_covid_json()
#    date_list = get_date_list(jsonobj)
#    print(date_list)
    daily_metrics = build_daily_metrics_india(jsonobj)
    df = get_df_metrics_india(daily_metrics)
    df = get_7day_moving_avg(df)
    print(df)

#    fig = px.line(df, x=df.index, y='test_confirm_rate')
    fig = px.line(df, x=df.index, y=df.test_confirm_rate)
    fig.update_layout(
        title="7 Day Moving Average of Covid-19 Daily Test Confirmation Rate in India",
        yaxis_title="Test Confirmation Rate",
        xaxis_title="Date",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )

    fig.show()
