import pandas as pd
import numpy as np


class ValueAndCostOfBoughtPositionCalculator:
    def __init__(self, calculation_source: pd.DataFrame):
        self.__calculation_source = calculation_source

    def append_value_and_cost(self) -> pd.DataFrame:
        self.__calculation_source = OriginalValueCalculator(self.__calculation_source.copy()).append_original_value()
        original_value_greater_or_equal_to_maintenance_margin_condition = \
            self.__get_original_value_greater_or_equal_to_maintenance_margin_condition()

        self.__calculation_source = ValueCalculator(
            self.__calculation_source.copy(), original_value_greater_or_equal_to_maintenance_margin_condition
        ).append_value()
        self.__calculation_source = CostCalculator(
            self.__calculation_source.copy(), original_value_greater_or_equal_to_maintenance_margin_condition
        ).append_cost()

        self.__calculation_source = self.__calculation_source.drop(['original_value'], axis=1)

        return self.__calculation_source

    def __get_original_value_greater_or_equal_to_maintenance_margin_condition(self):
        return self.__calculation_source['original_value'] >= self.__calculation_source['maintenance_margin']


class OriginalValueCalculator:
    def __init__(self, calculation_source):
        self.__calculation_source = calculation_source

    def append_original_value(self):
        self.__calculation_source.loc[:, 'original_value'] = self.__calculation_source['initial_margin'] + \
            (
                self.__calculation_source['close_price'] - self.__calculation_source['open_price']
            ) * self.__calculation_source['leverage'] * self.__calculation_source['unit']
        return self.__calculation_source


class ValueCalculator:
    def __init__(self, calculation_source, original_value_greater_or_equal_to_maintenance_margin_condition):
        self.__calculation_source = calculation_source
        self.__original_value_greater_or_equal_to_maintenance_margin_condition = \
            original_value_greater_or_equal_to_maintenance_margin_condition

    def append_value(self):
        self.__calculation_source.loc[:, 'value'] = np.where(
            self.__original_value_greater_or_equal_to_maintenance_margin_condition,
            self.__get_value_when_original_value_greater_or_equal_to_maintenance_margin(),
            self.__get_value_when_original_value_less_than_maintenance_margin()
        )

        return self.__calculation_source

    def __get_value_when_original_value_greater_or_equal_to_maintenance_margin(self):
        return self.__calculation_source['original_value']

    def __get_value_when_original_value_less_than_maintenance_margin(self):
        return self.__calculation_source['initial_margin']


class CostCalculator:
    def __init__(self, calculation_source, original_value_greater_or_equal_to_maintenance_margin_condition):
        self.__calculation_source = calculation_source
        self.__original_value_greater_or_equal_to_maintenance_margin_condition = \
            original_value_greater_or_equal_to_maintenance_margin_condition

    def append_cost(self):
        self.__calculation_source.loc[:, 'cost'] = np.where(
            self.__original_value_greater_or_equal_to_maintenance_margin_condition,
            self.__get_cost_when_original_value_greater_or_equal_to_maintenance_margin(),
            self.__get_cost_when_original_value_less_than_maintenance_margin()
        )

        return self.__calculation_source

    def __get_cost_when_original_value_greater_or_equal_to_maintenance_margin(self):
        return self.__calculation_source['initial_margin'] + self.__calculation_source['fee']

    def __get_cost_when_original_value_less_than_maintenance_margin(self):
        return self.__calculation_source['initial_margin'] + \
               (
                   self.__calculation_source['initial_margin'] - self.__calculation_source['original_value']
               ) + self.__calculation_source['fee']

