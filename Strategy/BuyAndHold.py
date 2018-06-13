from AssetMaintainer.AssetMaintainer import AssetMaintainer
from BackTesterContext.BackTesterContext import BackTesterContext
import pandas as pd
from datetime import datetime


class BuyAndHold:
    def __init__(self, asset_maintainer: AssetMaintainer, back_test_context: BackTesterContext, target_contract):
        self.__asset_maintainer = asset_maintainer
        self.__back_test_context = back_test_context
        self.target_contract = target_contract

    def make_decision(self, price_information: pd.DataFrame):

        if self.__asset_maintainer.current_position_status_maintainer.current_position_status.empty is True and \
                price_information.loc[price_information['contract'] == self.target_contract].empty is False:

            recent_month_of_target_contract = pd.to_datetime(
                price_information.loc[price_information['contract'] == self.target_contract]['delivery_month'],
                format='%Y%m'
            ).min()

            self.__back_test_context.send_order(
                pd.DataFrame(
                    [
                        {
                            'contract': self.target_contract,
                            'delivery_month': str(datetime.strftime(recent_month_of_target_contract, '%Y%m')),
                            'buy_position': 1,
                            'sell_position': 0
                        }
                    ]
                )
            )
