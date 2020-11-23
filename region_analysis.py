region = 'Salt Lake' ## use US for countrywide stats 

import fetchData
import pandas as pd

fetchData.nytData()
all_data = pd.read_csv('us-counties.csv')

if region == 'US':
    region_data = all_data.groupby('date').sum()[['cases','deaths']].reset_index().sort_values('date')
else:
    region_data = all_data[all_data['county'] == region].sort_values('date')

region_data['cases - deaths'] = region_data['cases'] - region_data['deaths']
region_data['new cases'] = region_data['cases'] - region_data['cases'].shift(1)
region_data['new deaths'] = region_data['deaths'] - region_data['deaths'].shift(1)
region_data['new cases - new deaths'] = region_data['new cases'] - region_data['new deaths'] 
covid_length = 21
region_data['current active'] = region_data['new cases - new deaths'].rolling(covid_length).sum()
region_data['infection rate'] = region_data['new cases']/region_data['current active'] 
region_data['infection rate weekly avg'] =region_data['infection rate'].rolling(7).mean()
region_data['case growth'] = region_data['new cases']/(region_data['cases'] - region_data['new cases'])

fig = region_data[region_data['date']>'2020-03-31'].plot(x = 'date', y = 'cases', legend = False).get_figure()
fig.savefig('chart/cases.jpg')
fig = region_data[region_data['date']>'2020-03-31'].plot(x = 'date', y = 'new cases', legend = False).get_figure()
fig.savefig('chart/new cases.jpg')
fig = region_data[region_data['date']>'2020-03-31'].plot(x = 'date', y = 'current active', legend = False).get_figure()
fig.savefig('chart/current active.jpg')
fig = region_data[region_data['date']>'2020-03-31'].plot(x = 'date', y = 'case growth', legend = False).get_figure()
fig.savefig('chart/case growth.jpg')
fig = region_data[region_data['date']>'2020-03-31'].plot(x = 'date', y = 'infection rate weekly avg', legend = False).get_figure()
fig.savefig('chart/infection rate weekly avg.jpg')

output = region_data[['date','cases','deaths','new cases','new deaths','current active','infection rate','infection rate weekly avg','case growth']]
output.to_csv('output - {}.csv'.format(region))
output.tail(7).to_csv('output - {} (last week).csv'.format(region))

import os, os.path
import win32com.client

if os.path.exists("daily covid report.xlsm"):
    xl=win32com.client.Dispatch("Excel.Application")
    xl.Workbooks.Open(os.path.abspath("daily covid report.xlsm"), ReadOnly=1)
    xl.Application.Run("excelsheet.xlsm!module1.prepareReport")
    xl.Application.Quit()
    del xl