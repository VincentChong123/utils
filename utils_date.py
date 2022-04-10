from datetime import datetime
from datetime import timedelta
import pandas as pd

day_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

#return df with from start to end, with df_date_format
def run_get_date_start2end(start_yyyymmdd, end_yyyymmdd, output_date_format = "%Y-%m-%d"):
    start = datetime.strptime(start_yyyymmdd,"%Y%m%d")
    end = datetime.strptime(end_yyyymmdd, "%Y%m%d")
    dict_date_day = {
        output_date_format: [],
        'day': []
    }

    while start < (end + timedelta(1)):
        dict_date_day[output_date_format].append(start)
        dict_date_day['day'].append(day_list[start.weekday()])

        start += timedelta(1)

    df = pd.DataFrame.from_dict(dict_date_day)
    df[output_date_format] = pd.to_datetime(df[output_date_format], "%Y-%m-%d")

    return df

if __name__ == '__main__':

    df = run_get_date_start2end('20100101', '20220208', output_date_format="%Y-%m-%d")
    df.rename(columns={"%Y-%m-%d": "date"}, inplace=True)
    print(df.head())
    print(df.head(-5))
    print(max(df.date.values))
