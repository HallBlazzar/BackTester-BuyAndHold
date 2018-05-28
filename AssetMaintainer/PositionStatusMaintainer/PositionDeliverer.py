import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta, WE


class PositionDeliverer:
    def __init__(self, current_position_status: pd.DataFrame, current_date: datetime, price_parameter: pd.DataFrame):
        self.__current_position_status = current_position_status
        self.__current_date = current_date
        self.__price_parameter = price_parameter

    def execute(self):
        third_wednesday = self.__current_date + relativedelta(day=1, weekday=WE(3))

        if self.__current_date >= third_wednesday and self.__current_position_status.empty is False:
            delivery_month = str(self.__current_date.strftime('%Y%m'))
            select_contract_reach_delivery_month = self.__current_position_status['delivery_month'] == delivery_month

            self.__current_position_status.loc[select_contract_reach_delivery_month, 'status'] = 'delivered'

        return self.__current_position_status
