import tabula
import re
import pandas as pd
from pathlib import Path
import datetime as dt
import mi_property_analyser as mpa

today_date = dt.datetime.today().strftime('%Y_%m_%d_%H%M%S')
p = Path(__file__).parents[0]

print(p)

# Change pdf name
df = tabula.read_pdf(p.joinpath("20201126 Waltham Forest Privated Public Register November 2020.pdf")
                     , pages='all'
                     , pandas_options = {'header': None})

print('length of df:' + str(len(df)))

# quit()

class SplitFields:
    def __init__(self, field):
        self.field = field

    @property
    def split_list(self):
        return re.split(r'([A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2})', self.field)

    @property
    def property_address(self):
        return ''.join(self.split_list[:len(self.split_list) - 1])

    @property
    def licence_holder(self):
        return self.split_list[-1]


complete_register = pd.concat(df, ignore_index=True)

# remove first line which contains header data
complete_register.drop([0], inplace=True)

# reset index after dropping row
complete_register.reset_index(drop=True, inplace=True)

# get property address from field
complete_register[5] = complete_register[1].apply(lambda x: SplitFields(x).property_address)

# get licence holder from field
complete_register[6] = complete_register.apply(lambda x: SplitFields(x[1]).licence_holder if pd.isnull(x[2]) else x[2], axis=1)

# created a df with columns to keep
final_df = complete_register[[0,5,6,3,4]].copy()

# rename columns
final_df.columns = ['ref_no', 'property_address', 'licence_holder', 'start_date', 'end_date']

print(final_df.head())

print('final df length: ' + str(len(final_df)))

final_df = final_df[final_df['property_address'] != '']

print('final df length: ' + str(len(final_df)))
final_df['postcode'] = final_df['property_address'].map(mpa.NearestStation.extract_postcode)


def nearest_station_wrapper(pc, n):
    try:
        return mpa.NearestStation(pc).find_nearest_station()[n]
    except KeyError:
        return None


final_df['nearest_station'] = final_df['postcode'].map(lambda x: nearest_station_wrapper(x, 0))
final_df['nearest_station_dist_miles'] = final_df['postcode'].map(lambda x: nearest_station_wrapper(x, 1))

# Write code to determine who has the most properties to their name
# print(final_df.groupby(['licence_holder'])['property_address'].count().head())

# Write code to determine station with the most properties nearby

# print(final_df.groupby(['nearest_station'])['property_address'].count().head())

# Save to csv

final_df.to_csv(p.joinpath(today_date + " waltham_forest_prpl_register.csv"), index=False)
