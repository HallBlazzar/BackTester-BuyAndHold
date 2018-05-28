import pandas as pd


class ValueAndCostOfSoldPositionCalculator:
    def __init__(self, calculation_source: pd.DataFrame):
        self.__calculation_source = calculation_source

    def append_value_and_cost(self):
        self.__calculation_source = ValueCalculator(self.__calculation_source.copy()).append_value()
        self.__calculation_source = CostCalculator(self.__calculation_source.copy()).append_cost()

        return self.__calculation_source


class ValueCalculator:
    def __init__(self, calculation_source):
        self.__calculation_source = calculation_source

    def append_value(self):
        self.__calculation_source.loc[:, 'value'] = \
            self.__calculation_source['value'] + \
            (
                self.__calculation_source['open_price'] -
                self.__calculation_source['close_price_of_previous_trading_date']
            ) * self.__calculation_source['leverage'] * self.__calculation_source['unit']

        return self.__calculation_source


class CostCalculator:
    def __init__(self, calculation_source):
        self.__calculation_source = calculation_source

    def append_cost(self):
        self.__calculation_source.loc[:, 'cost'] = self.__calculation_source['fee']

        return self.__calculation_source
