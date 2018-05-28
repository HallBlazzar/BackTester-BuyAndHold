import pandas as pd

from AssetMaintainer.PositionStatusMaintainer.CurrentPositionStatusMaintainer import \
    CurrentPositionStatusMaintainer
from AssetMaintainer.PositionStatusMaintainer.PositionStatusRecorder import \
    PositionStatusRecorder
from AssetMaintainer.CapitalMaintainer import CurrentCapitalMaintainer
from AssetMaintainer.CapitalMaintainer import CapitalRecorder


class AssetMaintainer:
    def __init__(self, initial_capital: int, price_parameter: pd.DataFrame):
        self.current_position_status_maintainer = CurrentPositionStatusMaintainer()
        self.position_status_recorder = PositionStatusRecorder()
        self.current_capital_maintainer = CurrentCapitalMaintainer(initial_capital)
        self.capital_recorder = CapitalRecorder()

        self.__price_parameter = price_parameter

    def update_asset(self, price_information: pd.DataFrame, trading_status: pd.DataFrame):
        self.current_position_status_maintainer.transform_trading_status_to_current_position_status(trading_status)
        self.current_position_status_maintainer.recalculate_value_and_cost(
            price_information=price_information.copy(), price_parameter=self.__price_parameter.copy()
        )
        self.current_position_status_maintainer.deliver_due_position(
            price_information=price_information.copy(), price_parameter=self.__price_parameter.copy()
        )
        self.current_capital_maintainer.update_current_capital(
            self.current_position_status_maintainer.calculation_source.copy()
        )
        self.capital_recorder.record_capital(
            capital=self.current_capital_maintainer.current_capital,
            date=price_information.at[0, 'date']
        )
        self.current_position_status_maintainer.settle_current_position()
        self.position_status_recorder.record_position_status(
            position_status=self.current_position_status_maintainer.current_position_status.copy(),
            date=price_information.at[0, 'date']
        )
