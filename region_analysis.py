#%%
from pylab import mpl
mpl.rcParams['font.sans-serif'] = 'Microsoft Yahei'
mpl.rcParams['axes.unicode_minus'] = False
#%%
import pandas as pd
all_data = pd.read_csv('us-counties.csv')
region_data = all_data[all_data['county'] == 'Salt Lake'].sort_values('date')
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
region_data_CN = region_data
region_data_CN = region_data_CN.rename(columns={
    'date'                          :'日期',
    'county'                        :'郡',
    'state'                         :'州',
    'cases'	                        :'总感染人数',
    'deaths'                        :'总死亡人数',
    'cases - deaths'                :'总感染人数 - 总死亡人数',
    'new cases'	                    :'新感染人数',
    'new deaths'                    :'新死亡人数',
    'new cases - new deaths'        :'新感染人数 - 新死亡人数',
    'current_active'	            :'当前感染人数',
    'infection rate'	            :'感染率',
    'infection rate weekly avg'	    :'感染率（周平均）',
    'case growth'	                :'总感染人数增长率'
})
region_data_CN.tail(7).to_csv('output.csv')

region_data_CN.tail(7)

# %%
