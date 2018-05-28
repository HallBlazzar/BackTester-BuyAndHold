import pandas as pd

from AssetMaintainer.ValueAndCostCalculator.ValueAndCostOfBoughtPositionCalculator import \
    ValueAndCostOfBoughtPositionCalculator
from AssetMaintainer.ValueAndCostCalculator.ValueAndCostOfHoldingPositionCalculator import \
    ValueAndCostOfHoldingPositionCalculator
from AssetMaintainer.ValueAndCostCalculator.ValueAndCostOfSoldPositionCalculator import \
    ValueAndCostOfSoldPositionCalculator


class ValueAndCostReCalculator:
    def __init__(self, current_position_status, price_information, price_parameter):
        self.__current_position_status = current_position_status
        self.__price_information = price_information
        self.__price_parameter = price_parameter

        self.__calculation_source = pd.DataFrame()

    def recalculate_value_and_cost(self) -> pd.DataFrame:
        self.__calculation_source = self.__current_position_status.merge(
            self.__price_information, on=['contract', 'delivery_month']
        )

        self.__calculation_source = self.__calculation_source.merge(
            self.__price_parameter, on=['contract']
        )

        self.__calculate_value_and_cost_for_every_status()

        return self.__calculation_source

    def __calculate_value_and_cost_for_every_status(self):
        status_and_calculator_pair = {
            'bought': ValueAndCostOfBoughtPositionCalculator,
            'sold': ValueAndCostOfSoldPositionCalculator,
            'holding': ValueAndCostOfHoldingPositionCalculator
        }

        for status, calculator in status_and_calculator_pair.items():
            self.__calculate_value_and_cost_for_single_status(status, calculator)

    def __calculate_value_and_cost_for_single_status(self, status, calculator):
        self.__calculation_source.loc[self.__calculation_source['status'] == status, :] = \
            calculator(
                self.__calculation_source.loc[self.__calculation_source['status'] == status]
            ).append_value_and_cost()
