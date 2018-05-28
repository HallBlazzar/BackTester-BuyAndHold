import pandas as pd

from AssetMaintainer.PositionStatusMaintainer.CurrentPositionStatusSettler import CurrentPositionStatusSettler
from AssetMaintainer.PositionStatusMaintainer.TradingStatusToCurrentPositionStatusTransformer import \
    TradingStatusToCurrentPositionStatusTransformer
from AssetMaintainer.PositionStatusMaintainer.ValueAndCostReCalculator import ValueAndCostReCalculator
from AssetMaintainer.PositionStatusMaintainer.PositionDeliverer import PositionDeliverer


class CurrentPositionStatusMaintainer:
    def __init__(
            self, initial_position_status=pd.DataFrame(
                columns=[
                    'contract', 'delivery_month', 'value', 'cost',
                    'close_price_of_previous_trading_date', 'status'
                ]
            )
    ):
        self.current_position_status = initial_position_status
        self.calculation_source = pd.DataFrame()

    def transform_trading_status_to_current_position_status(self, trading_status: pd.DataFrame):
        self.current_position_status = TradingStatusToCurrentPositionStatusTransformer(
            current_position_status=self.current_position_status,
            trading_status=trading_status
        ).update_current_position_status()

    def recalculate_value_and_cost(self, price_information, price_parameter):
        self.calculation_source = ValueAndCostReCalculator(
            current_position_status=self.current_position_status,
            price_information=price_information,
            price_parameter=price_parameter
        ).recalculate_value_and_cost()

    def deliver_due_position(self, price_information, price_parameter):
        self.calculation_source = PositionDeliverer(
            current_date=price_information.iloc[0, :]['date'],
            current_position_status=self.calculation_source,
            price_parameter=price_parameter
        ).execute()

    def settle_current_position(self):
        self.current_position_status = \
            CurrentPositionStatusSettler(self.calculation_source).settle_current_position_status()
