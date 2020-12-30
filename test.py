import region_analysis_alt
import pandas as pd

state = 'ut'
hos_data = region_analysis_alt.gather_state_hospitalized(state)



print(hos_data)