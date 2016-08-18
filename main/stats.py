import pandas as pd
from datetime import timedelta


class Statistics:
    def __init__(self, dw, date_from, date_to):
        self.dw = dw
        self.client = dw.get_client_info()
        self.date_from = date_from if date_from else self.client['date_from'] + timedelta(days=1)
        self.date_to = date_to if date_to else self.client['date_to']

    def get_data(self, date, by):
        shops = self.client['shops'].keys()
        data = self.dw.get_products_sale(
            shops=shops, by=by,
            date_from=date,
            date_to=date).T
        return data

    def receive_data(self):
        self.products1_turnover = self.get_data(self.date_from, 'turnover')
        self.products2_turnover = self.get_data(self.date_to, 'turnover')

        self.products1_qty = self.get_data(self.date_from, 'qty')
        self.products2_qty = self.get_data(self.date_to, 'qty')

        self.products1_receipts_qty = self.get_data(self.date_from, 'receipts_qty')
        self.products2_receipts_qty = self.get_data(self.date_to, 'receipts_qty')

    def get_statistics(self):
        turnover1 = float(self.products1_turnover.sum())
        turnover2 = float(self.products2_turnover.sum())
        qty1 = float(self.products1_qty.sum())
        qty2 = float(self.products2_qty.sum())
        receipts_qty1 = float(self.products1_receipts_qty.sum())
        receipts_qty2 = float(self.products2_receipts_qty.sum())
        avg_receipt1 = turnover1 / receipts_qty1
        avg_receipt2 = turnover2 / receipts_qty2

        indicators = ['turnover', 'qty', 'receipts_qty', 'avg_receipt']
        date1_statistics = pd.Series([turnover1, qty1, receipts_qty1, avg_receipt1],
                                     indicators,
                                     name=self.products1_turnover.columns[0].date())
        date2_statistics = pd.Series([turnover2, qty2, receipts_qty2, avg_receipt2],
                                     indicators,
                                     name=self.products2_turnover.columns[0].date())
        statistics = pd.concat([date2_statistics, date1_statistics], axis=1)
        statistics['% diff'] = 100 * (statistics[statistics.columns[0]] -
                                      statistics[statistics.columns[1]]) / \
                                      statistics[statistics.columns[1]]
        statistics['diff'] = statistics[statistics.columns[0]] - statistics[statistics.columns[1]]
        statistics.insert(0, 'indicators', indicators)
        return statistics

    def calc_difference(self):
        products_qty_diff = self.products2_qty[self.products2_qty.columns[0]] - \
                            self.products1_qty[self.products1_qty.columns[0]]
        products_qty_diff.name = 'qty_diff'

        products_turnover_diff = self.products2_turnover[self.products2_turnover.columns[0]] - \
                                 self.products1_turnover[self.products1_turnover.columns[0]]
        products_turnover_diff.name = 'turnover_diff'

        self.difference = pd.concat([products_qty_diff, products_turnover_diff], axis=1)
        self.difference = self.difference[self.difference['turnover_diff'] != 0].dropna()
        self.difference = self.difference.sort_values('turnover_diff', ascending=False)
        self.difference.insert(0, 'names', self.difference.index)

    def get_increase_products(self):
        return self.difference[self.difference['turnover_diff'] > 0]

    def get_decrease_products(self):
        return self.difference[self.difference['turnover_diff'] < 0]
