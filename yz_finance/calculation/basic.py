"""
Basic calculation for financial data
"""

import pandas as pd
import numpy as np


class BasicCalculation:

    # 1. drifts for data
    @staticmethod
    def drifts_linear(data: object) -> object:  # return a dataframe
        drifts = data / data.shift(1) - 1
        drifts = drifts.dropna()
        return drifts

    @staticmethod
    def drifts_log(data: object) -> object:  # return a dataframe
        drifts = np.log(data / data.shift(1))
        return drifts.dropna(axis=0, how='any', inplace=True)

    # 2. expected return for the data
    @staticmethod
    def expected_return_linear(data: object) -> object:
        drifts = BasicCalculation.drifts_linear(data)
        return drifts.mean()

    @staticmethod
    def expected_return_log(data: object) -> object:
        drifts = BasicCalculation.drifts_log(data)
        return drifts.mean()

    # 3. volatility
    @staticmethod
    def volatility_linear(data: object) -> object:
        drifts = BasicCalculation.drifts_linear(data)
        return drifts.std()

    @staticmethod
    def volatility_log(data: object) -> object:
        drifts = BasicCalculation.drifts_log(data)
        return drifts.std()

    @staticmethod
    def volatility_annualized_linear(data: object, annual: int = 52) -> object:
        volatility = BasicCalculation.volatility_linear(data)
        return volatility * np.sqrt(annual)

    @staticmethod
    def volatility_annualized_log(data: object, annual: int = 52) -> object:
        volatility = BasicCalculation.volatility_log(data)
        return volatility * np.sqrt(annual)

    # 4. 协方差矩阵
    @staticmethod
    def cov_matrix_linear(data: object) -> object:
        drifts = BasicCalculation.drifts_linear(data)
        return drifts.cov()

    @staticmethod
    def cov_matrix_log(data: object) -> object:
        drifts = BasicCalculation.drifts_log(data)
        return drifts.cov()

    # 5. 相关性矩阵
    @staticmethod
    def corr_matrix_linear(data: object) -> object:
        drifts = BasicCalculation.drifts_linear(data)
        return drifts.corr()

    @staticmethod
    def corr_matrix_log(data: object) -> object:
        drifts = BasicCalculation.drifts_log(data)
        return drifts.corr()

    # 6. 6个月滚动波动率
    @staticmethod
    def rolling_volatility_linear(data: object, period: int = 26, annual: int = 52) -> object:
        drifts = BasicCalculation.drifts_linear(data)
        output = drifts.rolling(period).std() * np.sqrt(annual)
        output.dropna(axis=0, how='any', inplace=True)
        return output

    @staticmethod
    def rolling_volatility_log(data: object, period: int = 26, annual: int = 52) -> object:
        drifts = BasicCalculation.drifts_log(data)
        output = drifts.rolling(period).std() * np.sqrt(annual)
        output.dropna(axis=0, how='any', inplace=True)
        return output

    # 7. 累计收益率表格（净值归一处理）
    @staticmethod
    def accumulate_return_linear(data: object) -> object:
        drifts = BasicCalculation.drifts_linear(data)
        output = (drifts + 1).cumprod()
        output.iloc[0, :] = 1
        return output

    # 8. 年化收益率
    @staticmethod
    def annualised_return(data: object, annual: int = 52) -> object:
        drifts = BasicCalculation.accumulate_return_linear(data)
        return drifts.iloc[-1, :] ** (annual / (data.shape[0] - 1)) - 1

    # 9. 夏普比率
    @staticmethod
    def sharpe(data: object, annual: int = 52) -> object:
        expected_return = BasicCalculation.expected_return_linear
        volatility = BasicCalculation.volatility_linear
        return (expected_return - 0.015) / volatility

    # 10. 超额收益
    @staticmethod
    def excess_return(data: object, index_data: object) -> object:
        drifts = BasicCalculation.drifts_linear(data)
        index_drifts = BasicCalculation.drifts_linear(index_data)

        for product in drifts.columns:
            drifts[product] = drifts[product] - index_drifts

        return return_table

    # 10. 累计超额收益
    @staticmethod
    def accumulate_excess_return(data: object, index_data: object) -> object:
        drifts = BasicCalculation.drifts_linear(data)
        index_drifts = BasicCalculation.drifts_linear(index_data)

        for product in drifts.columns:
            drifts[product] = drifts[product] - index_drifts

        output = (drifts + 1).cumprod()
        output.iloc[0, :] = 1
        output = output - 1
        return output
