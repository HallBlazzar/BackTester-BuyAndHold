import pandas as pd


class CurrentPositionStatusSettler:
    def __init__(self, calculation_source):
        self.__calculation_source = calculation_source

    def settle_current_position_status(self) -> pd.DataFrame:
        self.__calculation_source = self.__calculation_source[
            ~self.__calculation_source['status'].isin(['sold', 'delivered'])
        ].copy()
        self.__calculation_source.loc[:, 'status'] = 'holding'

        settled_current_position_status = self.__calculation_source[
            [
                'contract', 'delivery_month', 'value', 'cost',
                'close_price', 'status'
            ]
        ]
        settled_current_position_status = settled_current_position_status.rename(
            index=int, columns={'close_price': 'close_price_of_previous_trading_date'}
        )

        return settled_current_position_status.reset_index(drop=True)
