# this script is used to take the raw data, filter out some of the invaliud rows
# and create the additional synthetic columns for the sake of the application demo
#
import pandas as pd
import numpy as np

df = pd.read_csv('HospitalDischarge.csv')

new = df["age"].str.split("-", n = 1, expand = True)
df['age_lb'] = new[0].str[1:].apply(int)

df['readmission_count'] = np.where(df['readmitted']==False, 0, 1 + abs(round(df['age_lb']/30 - round(df['time_in_hospital']/10) - 2)))

df['length_of_stay'] = np.where(df['readmitted']==False, 0, round(df['age_lb']/20*2 + round(df['time_in_hospital']/5) + df['num_procedures']/2 ) )

# REMOVE some ROWS AND COLUMNS

df2 = df[ df['discharge_disposition_id'] != 'Expired' ]

df3 = df2.loc[0:500,]

df3.to_csv('data.csv', header=True, index=False)


