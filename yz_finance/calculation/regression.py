"""
The module for regression
"""

import pandas as pd
import statsmodels.api as sm


class Regression:

    # 1. OLS
    @staticmethod
    def OLS(y_input: object, x_input: object) -> object:
        return sm.OLS(y_input, sm.add_constant(x_input)).fit()
