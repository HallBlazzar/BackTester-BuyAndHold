import pandas as pd


class PositionStatusRecorder:
    def __init__(self):
        self.position_status_record = pd.DataFrame(
            columns=[
                'date',
                'contract', 'delivery_month', 'value', 'cost',
                'close_price_of_previous_trading_date', 'status'
            ]
        )

    def record_position_status(self, position_status: pd.DataFrame, date):
        position_status['date'] = date
        self.position_status_record = self.position_status_record.append(position_status, sort=False)
        self.position_status_record = self.position_status_record.reset_index(drop=True)
