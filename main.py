import pandas as pd
from datetime import datetime, timedelta

class TreadMonitor:
    gbce = {
        'stock_symbol': ['TEA', 'POP', 'ALE', 'GIN', 'JOE'],
        'type': ['Common', 'Common', 'Common', 'Preferred', 'Common'],
        'last_dividend': [0, 8, 23, 8, 13],
        'fixed_dividend': [None, None, None, 2, None],
        'per_value': [100, 100, 60, 100, 250]
    }
    gbce_df = pd.DataFrame(gbce)
    dividend_yield = {}
    pe_ratio = {}

    record_trande_df = pd.DataFrame(columns=['stock_symbol', 'quantity', 'txn_info', 'price', 'timestamp'])

    def cal_dividend_yeild(self, price):

        for index, row in self.gbce_df.iterrows():
            if row['type'] == 'Common':
                dividend_yeild = row['last_dividend'] / price
                self.dividend_yield[row['stock_symbol']] = dividend_yeild
            else:
                dividend_yeild = ((row['fixed_dividend']/100) * row['per_value'])/price
                self.dividend_yield[row['stock_symbol']] = dividend_yeild
        print('dividend yeid = ',self.dividend_yield)

    def cal_pe_ratio(self, price):
        for keys in self.dividend_yield:
            try:
                pe_ratio_value = round(price/self.dividend_yield[keys],2)
                self.pe_ratio[keys] = pe_ratio_value
            except:
                self.pe_ratio[keys] = None
        print('P/E Ratio = ', self.pe_ratio)

    def record_trade(self, **kwargs):

        self.record_trande_df = self.record_trande_df.append(kwargs, ignore_index=True)

    def cal_value_weighted_stock_price(self):
        created_time = datetime.utcnow() - timedelta(minutes=5)
        data = self.record_trande_df[(self.record_trande_df['timestamp'] > created_time) & (self.record_trande_df['timestamp'] < datetime.utcnow())]
        print("last five minutes Volume Weighted Stock Price = ",round((data['price'] * data['quantity']).sum()/data['quantity'].sum(axis=0), 2))

    def gbce_all_stocks(self):
        dict_gbce = {}
        df1 = self.record_trande_df.copy()
        df1['volume_weighted'] = (df1['price'] * df1['quantity'])
        df1.drop(['timestamp', 'price', 'txn_info'], axis=1, inplace=True)
        df1['rank'] = [1 for i in range(len(df1))]
        g = df1.set_index('stock_symbol').groupby('stock_symbol')
        for stock_name, stock_name_df in g:
            df2 = g.get_group(stock_name).apply(sum)
            # dict_gbce[f'{stock_name}']=(df2['volume_weighted'] / df2['quantity']) ** (1 / float(df2['rank']))
            dict_gbce[stock_name]=(df2['volume_weighted'] / df2['quantity']) ** (1 / float(df2['rank']))

        print('gbce all stock value = ', dict_gbce)


if __name__ == '__main__':
    abc = TreadMonitor()

    abc.cal_dividend_yeild(1) ## change 1 as a price you required
    abc.cal_pe_ratio(1) ## change 1 as a price you required
    abc.record_trade(stock_symbol='TEA', quantity=18, txn_info='S', price=18, timestamp=pd.to_datetime('now').replace(microsecond=0)) ## add records
    # abc.record_trade(stock_symbol='POP', quantity=10, txn_info='S', price=100, timestamp=pd.to_datetime('now').replace(microsecond=0))
    abc.record_trade(stock_symbol='POP', quantity=10, txn_info='S', price=100, timestamp=datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p'))
    abc.record_trade(stock_symbol='ALE', quantity=10, txn_info='B', price=100, timestamp=pd.to_datetime('now').replace(microsecond=0))
    abc.record_trade(stock_symbol='ALE', quantity=120, txn_info='B', price=100, timestamp=pd.to_datetime('now').replace(microsecond=0))
    abc.record_trade(stock_symbol='GIN', quantity=300, txn_info='S', price=2000, timestamp=pd.to_datetime('now').replace(microsecond=0))
    abc.cal_value_weighted_stock_price() # calculate value weighted price
    abc.gbce_all_stocks() # calculate gbce value


