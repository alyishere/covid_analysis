import requests
import pandas as pd
import time
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt
import matplotlib as mpl
COLOR = '#305496'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR

def analysis(region,pop = 1000000):
    region = region
    all_data = pd.read_csv('us-counties.csv')

    if region == 'US':
        region_data = all_data.groupby('date').sum()[['cases','deaths']].reset_index().sort_values('date')
    else:
        region_data = all_data[all_data['county'] == region].sort_values('date')

    region_data['date'] = region_data['date'].astype('datetime64')

    region_data['cases - deaths'] = region_data['cases'] - region_data['deaths']
    region_data['new cases'] = region_data['cases'] - region_data['cases'].shift(1)
    region_data['new deaths'] = region_data['deaths'] - region_data['deaths'].shift(1)
    region_data['death rate'] = region_data['deaths']/region_data['cases']

    region_data['new cases - new deaths'] = region_data['new cases'] - region_data['new deaths'] 
    covid_length = 21
    region_data['current active'] = region_data['new cases - new deaths'].rolling(covid_length).sum()

    region_data['infection rate'] = region_data['current active']/pop
    region_data['infection rate weekly avg'] =region_data['infection rate'].rolling(7).mean()
    region_data['case growth'] = region_data['new cases']/(region_data['cases'] - region_data['new cases'])
    
    sixMonthAgo = (datetime.today() - timedelta(days = 180)).strftime('%Y-%m-%d')
    region_data_last180days = region_data[region_data['date']>sixMonthAgo]

    output = region_data[['date','cases','deaths','new cases','new deaths','current active','infection rate','infection rate weekly avg','case growth']]
    output.to_csv('output - {}.csv'.format(region))
    output.tail(7).to_csv('output - {} (last week).csv'.format(region))

    return region_data_last180days

def plotChart(region_data, chart_name):
    
    # COLOR = 'blue'
    # mpl.rcParams['text.color'] = COLOR
    # mpl.rcParams['axes.labelcolor'] = COLOR
    # mpl.rcParams['axes.color'] = COLOR
    # mpl.rcParams['xtick.color'] = COLOR
    # mpl.rcParams['ytick.color'] = COLOR


    ax = region_data.plot(x = 'date', y = chart_name, legend = False, c = COLOR)
    ax.set_xlabel("")
    plt.xticks(rotation=30, fontsize=7) 
    right_side = ax.spines["right"]
    right_side.set_visible(False)
    top_side = ax.spines["top"]
    top_side.set_visible(False)
    import matplotlib.dates as mdates
    import matplotlib.ticker as mtick
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%m-%d'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    if region_data[chart_name].max() < 1:
        vals = ax.get_yticks()
        ax.set_yticklabels(['{:,.2%}'.format(x) for x in vals])
    else:
        vals = ax.get_yticks()    
        ax.set_yticklabels(['{:,}'.format(x) for x in vals])

    ax.spines['bottom'].set_color(COLOR)
    ax.spines['left'].set_color(COLOR)
    ax.tick_params(axis='x', colors=COLOR)
    ax.tick_params(axis='y', colors=COLOR)
    ax.yaxis.label.set_color(COLOR)
    ax.xaxis.label.set_color(COLOR)

    plt.savefig('chart/{}.png'.format(chart_name),dpi = 300)
    plt.clf() 

def excelReport():
    import os, os.path
    import win32com.client

    if os.path.exists("daily covid report.xlsm"):
        xl=win32com.client.Dispatch("Excel.Application")
        wb = xl.Workbooks.Open(os.path.abspath("daily covid report.xlsm"), ReadOnly=1)
        xl.Application.Run("'daily covid report.xlsm'!Module1.prepareReport_v")
        wb.Close(True)
        del xl

def gather_state_hospitalized(state):
    link = 'https://api.covidtracking.com/v1/states/{}/daily.json'.format(state)

    response = requests.get(link,
        headers={'Accept': 'application/json'}
    )
    json_response = response.json()
    hos_data = pd.DataFrame(json_response)[['date','hospitalizedCurrently','hospitalizedIncrease']]
    hos_data['date'] = pd.to_datetime(hos_data['date'],format = "%Y%m%d")

    sixMonthAgo = (datetime.today() - timedelta(days = 180)).strftime('%Y-%m-%d')
    hos_data_last180days = hos_data[hos_data['date']>sixMonthAgo]
    
    return hos_data_last180days

def output_hospitalizations(state):
    hos_data = gather_state_hospitalized(state).head(7).sort_values('date',ascending=True)
    hos_data.to_csv('hospitalizations - {}.csv'.format(state))


