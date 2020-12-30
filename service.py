pop = 1120805
county = 'Salt Lake'
state = 'ut'

download_data = True

if download_data:
    import fetchData
    fetchData.nytData()

import region_analysis_alt

data = region_analysis_alt.analysis(county,pop)
hos_data = region_analysis_alt.gather_state_hospitalized(state)

print('Data processed.')

region_analysis_alt.plotChart(hos_data, 'hospitalizedCurrently')
region_analysis_alt.plotChart(data,'cases')
region_analysis_alt.plotChart(data,'new cases')
region_analysis_alt.plotChart(data,'current active')
region_analysis_alt.plotChart(data,'case growth')
region_analysis_alt.plotChart(data,'infection rate weekly avg')

region_analysis_alt.excelReport()

print('Report saved.')