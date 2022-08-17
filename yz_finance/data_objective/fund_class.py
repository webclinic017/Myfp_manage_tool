"""
product class module
"""

import pandas as pd


class Fund:
    """
    应包含

    Attribute:
    - 净值数据
    - fund_code
    - 所属策略
    - 是否为公司产品
    - 所属池子
    """

    def __init__(self,
                 fund_name: str = None,
                 company: str = None,
                 prices_data=None,
                 fund_code: int = None,
                 reg_num: str = None,
                 strategy: str = None,
                 is_myfp_product: bool = None,
                 pool: str = None):
        self.fund_name = fund_name
        self.company = company
        self.prices_data = prices_data
        self.fund_code = fund_code
        self.reg_num = reg_num
        self.strategy = strategy
        self.is_myfp_product = is_myfp_product
        self.pool = pool
        # not init attribute
        self.accumulate_price = None

    # --------- Attributes ---------
    def add_fund_name(self, fund_name):
        self.fund_name = fund_name

    def add_prices_data(self, prices_data):
        self.prices_data = prices_data

    def add_fund_code(self, fund_code: int):
        self.fund_code = fund_code

    def add_reg_num(self, reg_num: str):
        self.reg_num = reg_num

    def add_strategy(self, strategy: str):
        self.strategy = strategy

    def add_is_myfp_product(self, is_myfp_product: bool):
        self.is_myfp_product = is_myfp_product

    def add_pool(self, pool: str):
        self.pool = pool

    # --------- Methods ---------
    """
    # 数据
        - 读取数据
        - 获取基金fund_code
        - 更新数据
        - 保存数据
    """

    def read_data_csv(self, path: str):
        self.prices_data = pd.read_csv(path)
        self.accumulate_price = self.prices_data[f'{self.fund_name}累计净值'].copy()

    def get_fund_code(self):
        self.fund_code = kf.get_fund_code_by_name(self.fund_name)

    def save_date(self, path):
        self.prices_data.to_csv(f'{path}/{self.fund_name}_price.csv')

        fund_info = pd.Series([self.fund_name,
                               self.fund_code,
                               self.reg_num,
                               self.strategy,
                               self.is_myfp_product,
                               self.pool_50,
                               self.pool_200],
                              index=['基金名称', 'fund_code', '注册编号', '一级策略', '弘酬产品', '50池', '200池'])

        fund_info.to_csv(f'{path}/{self.fund_name}_info.csv')
