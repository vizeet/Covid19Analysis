import requests
import json
import pandas as pd
import plotly.express as px

URL = 'https://api.covid19india.org/v3/data-all.json'

def get_covid_json():
    global URL

    r = requests.get(url = URL)
    jsonobj = r.json()
#    print(json.dumps(jsonobj, indent = 4))

    return jsonobj

def build_metrics(jsonobj: dict):
    code_map = {}
    with open('code_name_map.json', 'rt') as code_map_f:
        code_map = json.load(code_map_f)

    metrics_list = []
    for date in jsonobj:
        for code in jsonobj[date]:
            if 'delta' in jsonobj[date][code]:
                delta = jsonobj[date][code]['delta']
                if 'tested' in delta and 'confirmed' in delta:
                    metrics = {}
                    metrics['metrics'] = code_map[code]
                    metrics['date'] = date
                    metrics['confirmed'] = delta['confirmed']
                    metrics['tested'] = delta['tested']
                    metrics['test_confirm_rate'] = (delta['confirmed'] * 100) / delta['tested']
                    metrics_list.append(metrics)
    return  metrics_list

def get_df_metrics(jsonobj: dict):
    df = pd.DataFrame.from_dict(jsonobj, orient='columns')

    grouped = df.groupby('metrics')
    newdf = pd.DataFrame(columns=['metrics', 'date', 'confirmed', 'tested', 'test_confirm_rate'])
    for metrics, df in grouped:
        print(metrics)
        df = df.rolling(7, on = 'date').mean().dropna()
        df['metrics'] = metrics
        newdf = newdf.append(df)

    return newdf

if __name__ == '__main__':
    jsonobj = get_covid_json()
    metrics_list = build_metrics(jsonobj)
    df = get_df_metrics(metrics_list)
    fig = px.line(df, x=df.date, y=df.test_confirm_rate, color = df.metrics)
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
