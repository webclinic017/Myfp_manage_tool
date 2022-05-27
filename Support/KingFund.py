"""
KingFund server connection module
@author: Yanzhong Huang
Date: 9 Sep 2021
Update: 28 March 2022, combine multiple equity method
"""

import sys
import pandas as pd
import pymssql


class KingFund:

    def __init__(self):
        connect = pymssql.connect('10.20.34.122', 'su', 'ysmz,.123', 'KingFund_DB_New')  # Define connection

        # connection result
        if connect:  # print out connection result
            print('connected')
        else:
            print("connection failed")
            sys.exit()

        self.cursor = connect.cursor()

    def get_fund_code_by_name(self, fund_name):
        # get fund code from KingFund
        sql = f"SELECT all [ProductName], [RegNum], [FundCode] FROM [KingFund_DB_New].[dbo].[PF_FundInfo] " \
              f"WHERE ProductName LIKE '%{fund_name}%'"
        self.cursor.execute(sql)
        output = self.cursor.fetchall()

        # build a series store the output
        if output:
            output = pd.DataFrame(output, columns=['基金名称', '备案编号', 'fund_code'])
            output.set_index('基金名称', inplace=True)
            # 金方数据库乱码问题，解决日期20220510
            output.index = [_.encode('latin1').decode('gbk') for _ in output.index]
        else:
            print(f'没查询到对应标的，查询标的名称：{fund_name}')
            output = pd.DataFrame({'基金名称': [fund_name], '备案编号': '无结果', 'fund_code': '无结果'})
            output.set_index('基金名称', inplace=True)

        return output

    def get_fund_code_by_regnum(self, regnum):
        # get fund code from KingFund
        sql = f"SELECT all [ProductName], [RegNum], [FundCode] FROM [KingFund_DB_New].[dbo].[PF_FundInfo] " \
              f"WHERE RegNum='{regnum}'"
        self.cursor.execute(sql)
        output = self.cursor.fetchall()

        # build a series store the output
        if output:
            output = pd.DataFrame(output, columns=['基金名称', '备案编号', 'fund_code'])
            output.set_index('基金名称', inplace=True)
            # 金方数据库乱码问题，解决日期20220510
            output.index = [_.encode('latin1').decode('gbk') for _ in output.index]
        else:
            print(f'没查询到对应标的，查询标的备案编号：{regnum}')
            output = pd.DataFrame({'基金名称': '无结果', '备案编号': regnum, 'fund_code': '无结果'})
            output.set_index('基金名称', inplace=True)

        return output

    def get_equity_price(self, fund_name, fund_code, start='', end=''):
        if start and end:
            sql = f"SELECT [DealDate], [UnitEquity], [AccumulateEquity], [AdjustedEquity] " \
                  f"FROM [KingFund_DB_New].[dbo].[PF_TotalNetValue] " \
                  f"WHERE [FundCode]='{fund_code}' AND ([DealDate] BETWEEN '{start}' AND '{end}')"
            self.cursor.execute(sql)
            output = self.cursor.fetchall()
            if output:
                output = pd.DataFrame(output,
                                      columns=['date',
                                               f'{fund_name}单位净值',
                                               f'{fund_name}累计净值',
                                               f'{fund_name}复权净值'])
                output.set_index('date', drop=True, inplace=True)
                output.sort_index(ascending=True, inplace=True)

                # 更改output数据类型
                output = output.astype('float')
            else:
                print(f'没查询到对应标的，查询标的代码：{fund_name}: {fund_code}')
            return output
        else:
            sql = f"SELECT [DealDate], [UnitEquity], [AccumulateEquity], [AdjustedEquity] " \
                  f"FROM [KingFund_DB_New].[dbo].[PF_TotalNetValue] " \
                  f"WHERE [FundCode]='{fund_code}'"
            self.cursor.execute(sql)
            output = self.cursor.fetchall()
            if output:
                output = pd.DataFrame(output,
                                      columns=['date',
                                               f'{fund_name}单位净值',
                                               f'{fund_name}累计净值',
                                               f'{fund_name}复权净值'])
                output.set_index('date', drop=True, inplace=True)
                output.sort_index(ascending=True, inplace=True)

                # 更改output数据类型
                output = output.astype('float')
            else:
                print(f'没查询到对应标的，查询标的代码：{fund_name}: {fund_code}')
            return output

    def test(self):
        fund_code_df = self.get_fund_code_by_name('盛冠达CTA基本面进取3号')
        print(fund_code_df)

        fund_code_df_by_reg = self.get_fund_code_by_regnum('SJB072')
        print(fund_code_df_by_reg)

        fund_price = self.get_equity_price(fund_code_df_by_reg.index[0], fund_code_df_by_reg['fund_code'][0],
                                           start='20191129', end='20201231')
        print(fund_price.head())


if __name__ == '__main__':
    kf = KingFund()
    kf.test()
