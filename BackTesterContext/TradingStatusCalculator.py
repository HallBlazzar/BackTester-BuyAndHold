import pandas as pd
import random


class TradingStatusCalculator:
    def __init__(self, success_rate: int):
        self.__success_rate = success_rate

    def append_trading_status(
            self, price_information_of_current_date: pd.DataFrame, order: pd.DataFrame
    ) -> pd.DataFrame:
        trading_status = self.get_trading_status(order)
        price_information_with_trading_status = pd.merge(
            price_information_of_current_date, trading_status, on='contract'
        )

        return price_information_with_trading_status

    def get_trading_status(self, order: pd.DataFrame) -> pd.DataFrame:
        order = order.rename(index=int, columns={"buy_position": "bought_position", "sell_position": "sold_position"})
        order[['bought_position', 'sold_position']] = order[['bought_position', 'sold_position']].apply(
            self.__calculate_trading_status_of_single_merchandise_on_target_series
        )

        return order

    def __calculate_trading_status_of_single_merchandise_on_target_series(self, target_series: pd.Series) -> pd.Series:
        return target_series.apply(self.__calculate_trading_status_of_single_merchandise)

    def __calculate_trading_status_of_single_merchandise(self, requirement: int) -> int:
        filled_requirement = 0

        for _ in range(requirement):
            if random.randint(0, 99) < self.__success_rate:
                filled_requirement += 1

        return filled_requirement
