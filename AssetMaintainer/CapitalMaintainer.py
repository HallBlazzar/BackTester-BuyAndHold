import pandas as pd


class CurrentCapitalMaintainer:
    def __init__(self, initial_capital=0):
        self.current_capital = initial_capital

    def update_current_capital(self, calculation_source: pd.DataFrame):
        earned_from_sold_position = calculation_source.loc[
            calculation_source['status'].isin(['sold', 'delivered']),
            'value'
        ].sum()
        total_cost = calculation_source['cost'].sum()

        self.current_capital = self.current_capital + earned_from_sold_position - total_cost


class CapitalRecorder:
    def __init__(self):
        self.capital_record = pd.DataFrame(
            columns=['date', 'capital']
        )

    def record_capital(self, capital: int, date):
        self.capital_record = self.capital_record.append(
            pd.DataFrame(
                [
                    {
                        'date': date,
                        'capital': capital
                    }
                ]
            ),
            sort=False
        )
        self.capital_record = self.capital_record.reset_index(drop=True)
