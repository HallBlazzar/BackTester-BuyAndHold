import pandas as pd
from datetime import datetime, timedelta
from dateutil.rrule import rrule, DAILY


class PriceInformationGenerator:
    def __init__(self, data_source: pd.DataFrame):
        self.__data_source = data_source

    def generate_price_information(self, start_date: datetime, end_date: datetime):
        for target_day in rrule(freq=DAILY, dtstart=start_date, until=end_date):
            next_target_day = target_day + timedelta(days=1)
            price_information = self.__data_source[
                (self.__data_source['date'] >= target_day) &
                (self.__data_source['date'] < next_target_day)
            ]

            if price_information.empty is False:
                yield price_information
