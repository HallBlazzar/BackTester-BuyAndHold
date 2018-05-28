import pandas as pd


class BackTesterContext:
    def __init__(self, price_information_generator, trading_status_calculator):
        self.__price_information_generator = price_information_generator
        self.__trading_status_calculator = trading_status_calculator

        self.order = None
        self.__reset_order()

    def move_to_next_day(self):
        for price_information_of_current_day in self.__price_information_generator:
            trading_status = self.__trading_status_calculator.get_trading_status(self.order)
            self.__reset_order()

            yield (price_information_of_current_day.reset_index(drop=True), trading_status)

    def send_order(self, order: pd.DataFrame):
        self.order = order

    def __reset_order(self):
        self.order = pd.DataFrame(
            columns=['contract', 'delivery_month', 'buy_position', 'sold_position']
        )
