import pandas as pd


class TradingStatusToCurrentPositionStatusTransformer:
    def __init__(self, current_position_status, trading_status):
        self.__current_position_status = current_position_status
        self.__trading_status = trading_status

    def update_current_position_status(self) -> pd.DataFrame:
        for index, trading_status_of_single_contract in self.__trading_status.iterrows():
            self.__current_position_status = TradingStatusOfSingleContractToCurrentPositionStatusTransformer(
                current_position_status=self.__current_position_status,
                trading_status_of_single_contract=trading_status_of_single_contract
            ).execute()

        return self.__current_position_status


class TradingStatusOfSingleContractToCurrentPositionStatusTransformer:
    def __init__(self, current_position_status: pd.DataFrame, trading_status_of_single_contract: pd.DataFrame):
        self.__current_position_status = current_position_status
        self.__trading_status_of_single_contract = trading_status_of_single_contract

    def execute(self) -> pd.DataFrame:
        contract = self.__trading_status_of_single_contract['contract']
        delivery_month = self.__trading_status_of_single_contract['delivery_month']
        bought_position = int(self.__trading_status_of_single_contract['bought_position'])
        sold_position = int(self.__trading_status_of_single_contract['sold_position'])

        self.__add_bought_position(
            contract=contract, delivery_month=delivery_month, number_of_bought_position=bought_position
        )

        self.__change_holding_positions_to_sold(
            contract=contract, delivery_month=delivery_month, number_of_sold_position=sold_position
        )

        return self.__current_position_status

    def __add_bought_position(self, contract, delivery_month, number_of_bought_position: int):
        self.__current_position_status = self.__current_position_status.append(
            pd.DataFrame(
                data=[
                    {
                        'contract': contract,
                        'delivery_month': delivery_month,
                        'status': 'bought'
                    } for _ in range(number_of_bought_position)
                ]
            ), sort=False
        )
        self.__current_position_status = self.__current_position_status.reset_index(drop=True)

    def __change_holding_positions_to_sold(self, contract, delivery_month, number_of_sold_position: int):
        target_contract = self.__current_position_status.loc[
            (self.__current_position_status['contract'] == contract) &
            (self.__current_position_status['delivery_month'] == delivery_month)
        ]

        index_of_sold_contract = target_contract.index.values[0: number_of_sold_position]

        for index in index_of_sold_contract:
            self.__current_position_status.at[index, 'status'] = 'sold'
