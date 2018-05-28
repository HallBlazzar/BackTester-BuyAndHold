from BackTesterContext.PriceInformationGenerator import PriceInformationGenerator
from BackTesterContext.TradingStatusCalculator import TradingStatusCalculator
from BackTesterContext.BackTesterContext import BackTesterContext
from AssetMaintainer.AssetMaintainer import AssetMaintainer
from Strategy.BuyAndHold import BuyAndHold

import pandas as pd
import os
from datetime import datetime


if __name__ == '__main__':
    data_source = pd.read_msgpack(os.path.join('Source', 'PriceInformation', '1998to2016.msg'))
    data_source['date'] = pd.to_datetime(data_source['date'], format="%Y-%m-%d")
    data_source['delivery_month'] = data_source['delivery_month'].astype('str')

    back_test_context = BackTesterContext(
        price_information_generator=PriceInformationGenerator(data_source).generate_price_information(
            start_date=datetime.strptime('1998/07/21', '%Y/%m/%d'),
            end_date=datetime.strptime('2016/12/30', '%Y/%m/%d')
        ),
        trading_status_calculator=TradingStatusCalculator(success_rate=100)
    )

    asset_maintainer = AssetMaintainer(
        initial_capital=1000000, price_parameter=pd.read_csv(os.path.join('Source', 'price_parameter.csv'))
    )

    buy_and_hold = BuyAndHold(
        asset_maintainer=asset_maintainer, back_test_context=back_test_context, target_contract='TX'
    )

    for price_information, trading_status in back_test_context.move_to_next_day():
        print('----------{}----------'.format(price_information.iloc[0, :]['date']))
        asset_maintainer.update_asset(price_information, trading_status)
        # print(asset_maintainer.current_position_status_maintainer.current_position_status)
        buy_and_hold.make_decision(price_information)

    asset_maintainer.position_status_recorder.position_status_record.to_msgpack(
        os.path.join('Source', 'result', 'position_status_record.msg')
    )

    asset_maintainer.capital_recorder.capital_record.to_msgpack(
        os.path.join('Source', 'result', 'capital_record.msg')
    )
