"""
for data filter and clean
"""

import pandas as pd


class Clean:

    # 1. MAD, mean absolute deviation
    @staticmethod
    def filter_outlier_MAD(data: object, n: int = 5) -> object:
        median = data.median()
        mad = ((data - median).abs()).median()
        min_range = median - n * mad
        max_range = median + n * mad
        return data.clip(lower=min_range, upper=max_range, axis=1)

    # 2 3sigma method
    @staticmethod
    def filter_outliers_sigma(data: object, n: int = 3) -> object:
        mean = data.mean()
        sigma = data.std()
        min_range = mean - n * sigma
        max_range = mean + n * sigma
        return data.clip(lower=min_range, upper=max_range, axis=1)

    # 3. percentile method
    # @staticmethod
    # def exclude_outliers_percentile(data: object,
    #                                 min: float = 0.025,
    #                                 max: float = 0.975) -> object:
    #     for column in data.columns:
    #         sorted_data = data[column].sort_values()
    #
    #     return data.clip(lower=min_range, upper=max_range, axis=1)


class Standardized:

    # 12. 标准化数据
    @staticmethod
    def normalized(data: object) -> object:
        mean = data.mean()
        sigma = data.std()
        return (data - mean) / sigma
