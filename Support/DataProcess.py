"""
数据处理
Author: Yanzhong Huang
Latest update: 5 Nov 2021
"""

import pandas as pd
import numpy as np


class DataProcess:

    # 1. 每期收益率表格
    @staticmethod
    def return_table(data):
        output = data / data.shift(1) - 1
        return output

    # 2. 各标的期望收益率
    @staticmethod
    def expected_return(data, annual=52):
        return_table = DataProcess.return_table(data)
        output = (return_table.mean() + 1) ** annual - 1
        return output

    # 3. 各标的波动率
    @staticmethod
    def volatility(data, annual=52):
        return_table = DataProcess.return_table(data)
        output = return_table.std() * np.sqrt(annual)
        return output

    # 4. 协方差矩阵
    @staticmethod
    def cov_matrix(data):
        return_table = DataProcess.return_table(data)
        output = return_table.cov()
        return output

    # 5. 相关性矩阵
    @staticmethod
    def corr_matrix(data):
        return_table = DataProcess.return_table(data)
        output = return_table.corr()
        return output

    # 6. 6个月滚动波动率
    @staticmethod
    def rolling_volatility(data, period=26, annual=52):
        return_table = DataProcess.return_table(data)
        output = return_table.rolling(period).std() * np.sqrt(annual)
        output.dropna(axis=0, how='any', inplace=True)
        return output

    # 7. 累计收益率表格（净值归一处理）
    @staticmethod
    def accumulate_return(data):
        return_table = DataProcess.return_table(data)
        output = (return_table + 1).cumprod()
        output.iloc[0, :] = 1
        return output

    # 8. 年化收益率
    @staticmethod
    def annualised_return(data, annual=52):
        return_table = DataProcess.accumulate_return(data)
        output = return_table.iloc[-1, :] ** (annual / (data.shape[0] - 1)) - 1
        return output

    # 9. 夏普比率
    @staticmethod
    def sharpe(data, annual=52):
        expected_return = DataProcess.expected_return(data, annual=annual)
        volatility = DataProcess.volatility(data, annual=annual)
        output = (expected_return - 0.015) / volatility
        return output

    # 10. 超额收益
    @staticmethod
    def excess_return(data, index_data):
        return_table = DataProcess.return_table(data)
        index_return_table = DataProcess.return_table(index_data)

        for product in return_table.columns:
            return_table[product] = return_table[product] - index_return_table

        return return_table

    # 10. 累计超额收益
    @staticmethod
    def accumulate_excess_return(data, index_data):
        return_table = DataProcess.return_table(data)
        index_return_table = DataProcess.return_table(index_data)

        for product in return_table.columns:
            return_table[product] = return_table[product] - index_return_table

        output = (return_table + 1).cumprod()
        output.iloc[0, :] = 1
        output = output - 1
        return output


# test
if __name__ == '__main__':
    test = pd.read_excel('data for test.xlsx', index_col=0)
    return_table = DataProcess.excess_return(test, test.iloc[:, 0])
    print(return_table)
    print(type(return_table))

    return_table = DataProcess.accumulate_excess_return(test, test.iloc[:, 0])
    print(return_table)
    print(type(return_table))