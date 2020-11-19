#%%
import pandas as pd
all_data = pd.read_csv('us-counties.csv')

us_data = all_data.groupby('date').sum()[['cases','deaths']].reset_index().sort_values('date')
region_data = us_data
#%%
region_data['cases - deaths'] = region_data['cases'] - region_data['deaths']
region_data['new cases'] = region_data['cases'] - region_data['cases'].shift(1)
region_data['new deaths'] = region_data['deaths'] - region_data['deaths'].shift(1)
region_data['new cases - new deaths'] = region_data['new cases'] - region_data['new deaths'] 
covid_length = 21
region_data['current_active'] = region_data['new cases - new deaths'].rolling(covid_length).sum()
region_data['infection rate'] = region_data['new cases']/region_data['current_active'] 
region_data['infection rate weekly avg'] =region_data['infection rate'].rolling(7).mean()
region_data['case growth'] = region_data['new cases']/(region_data['cases'] - region_data['new cases'])
region_data.tail(7)
# %%
region_data[region_data['date']>'2020-03-31'].plot(x = 'date', y = 'cases')
region_data[region_data['date']>'2020-03-31'].plot(x = 'date', y = 'new cases')
region_data[region_data['date']>'2020-03-31'].plot(x = 'date', y = 'current_active')
region_data[region_data['date']>'2020-03-31'].plot(x = 'date', y = 'case growth')
region_data[region_data['date']>'2020-03-31'].plot(x = 'date', y = 'infection rate weekly avg')

# %%


