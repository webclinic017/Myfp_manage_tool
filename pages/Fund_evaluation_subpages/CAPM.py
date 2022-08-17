import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from yz_finance.data_get.kingfund import KingFund
from yz_finance.data_objective.fund_class import Fund
from yz_finance.calculation.basic import BasicCalculation
from yz_finance.calculation.data_clean import Clean, Standardized
from yz_finance.calculation.regression import Regression
from yz_finance.data_get.tushare_pro import TushareData
from yz_finance.utility.matplotlib_ch_font import matplot_ch_font

matplot_ch_font()
ts = TushareData()


def header():
    st.write('---')
    st.subheader('CAPM模型')


# 链接数据库及池子信息
def connection():
    pool = pd.read_excel('data/Funds list/pool.xlsx', index_col=0)

    try:
        kf = KingFund()  # 实例化kingfund模块
    except:
        kf = None
        st.warning('无法连接至金方数据库，请在公司内网重试！')

    return pool, kf


# 选择基金
def fund_selection(pool):
    selected_fund_name = st.selectbox(label='请选择基金', options=pool.index)
    selected_fund = Fund(fund_name=selected_fund_name,
                         company=pool.loc[selected_fund_name, '基金公司'],
                         fund_code=pool.loc[selected_fund_name, 'fund_code'],
                         reg_num=pool.loc[selected_fund_name, '备案编号'],
                         strategy=pool.loc[selected_fund_name, '二级策略'],
                         pool=pool.loc[selected_fund_name, '所属池'])

    return selected_fund


# 选择指数
def index_selection():
    index_dict = {'沪深300': '000300.SH',
                  '中证500': '000905.SH',
                  '中证1000': '000852.SH',
                  '创业板': '399006.SZ',
                  '中小100': '399005.SZ',
                  '中证100': '399903.SZ',
                  '上证50': '000016.SH'
                  }
    selected_index_name = st.selectbox(label='请选择基准指数', options=index_dict.keys())
    index_data = ts.weekly_index(ts_code=index_dict[selected_index_name])
    index_data.set_index('trade_date', inplace=True)
    index_data.index = pd.to_datetime(index_data.index).date
    index_data = index_data['close']
    index_data.name = selected_index_name
    return index_data


# 获取选择基金数据
def get_fund_data(kf, selected_fund):
    try:
        fund_data = kf.get_equity_price(fund_name=selected_fund.fund_name,
                                        fund_code=selected_fund.fund_code)
        fund_data.index = pd.to_datetime(fund_data.index).date
    except:
        st.warning('连接失败，请重试！')

    selected_fund.prices_data = fund_data


# 基础信息
def basic_info(selected_fund, index_data):
    st.subheader('基本信息')
    st.markdown(f'##### {selected_fund.fund_name} ')

    col_1, col_2 = st.columns(2)
    with col_1:
        st.markdown(f""" 
        所属公司：{selected_fund.company}  
        备案编号：{selected_fund.reg_num}  
        二级策略：{selected_fund.strategy}  
        所属池：{selected_fund.pool}
        """)
    with col_2:
        # 合并指数与基金数据
        data = pd.concat([selected_fund.prices_data.iloc[:, 2], index_data], axis=1, join='inner')

        # 计算展示信息

        duration = selected_fund.prices_data.index[-1] - selected_fund.prices_data.index[0]  # 成立年份

        # st.write(BasicCalculation.drifts_linear(data))

        expected_return = BasicCalculation.expected_return_linear(data)
        annualised_return = round(((1 + expected_return) ** 52 - 1) * 100, 2)
        vol = round(BasicCalculation.volatility_linear(data) * np.sqrt(52) * 100, 2)

        st.markdown(f"""
        成立时长：{round(int(duration.days) / 365.2425, 1)}年  
        年化收益：{annualised_return[0]}% ({annualised_return[1]}%, 同期基准指数)  
        年化波动率：{vol[0]}% ({vol[1]}%, 同期基准指数)  
        夏普比率：{round((annualised_return - 1.5) / vol, 2)[0]} 
        ({round((annualised_return - 1.5) / vol, 2)[1]}, 同期基准指数)  
        """)


def process_data(data: object) -> object:
    exclude_outlier_data = Clean.filter_outlier_MAD(data=data, n=5)
    normalized_data = Standardized.normalized(exclude_outlier_data)
    return normalized_data


def plot(fund: object, index_data: object):
    st.write('---')
    # 合并净值及指数
    data = pd.concat([fund.prices_data.iloc[:, 2], index_data], axis=1, join='inner')
    data_drifts = BasicCalculation.drifts_linear(data=data)
    # data_drifts_normalized = process_data(data=data_drifts)

    # 线性回归
    regression = Regression.OLS(x_input=data_drifts.iloc[:, 1],
                                y_input=data_drifts.iloc[:, 0])

    # regression_normalized = Regression.OLS(x_input=data_drifts_normalized.iloc[:, 1],
    #                                                     y_input=data_drifts_normalized.iloc[:, 0])

    def plot_hist(data_hist):
        fig, ax = plt.subplots()
        ax.hist(data_hist, bins=20)
        ax.legend(data_hist.columns)
        ax.grid('both')
        st.pyplot(fig)

    def plot_scatter(data_scatter, beta=regression.params[1], alpha=regression.params[0]):
        fig, ax = plt.subplots()
        ax.scatter(data_scatter.iloc[:, 1], data_scatter.iloc[:, 0])
        # ax.legend(data_scatter.columns)
        ax.grid('both')
        plt.xlabel(data_scatter.columns[1])
        plt.ylabel(data_scatter.columns[0])
        # best fit line
        plt.plot(data_scatter.iloc[:, 1], data_scatter.iloc[:, 1] * beta + alpha, color='r')
        st.pyplot(fig)

    # 显示图

    st.markdown('##### 原始数据-收益直方图')
    plot_hist(data_drifts)
    st.markdown('##### 原始数据-收益散点图')
    plot_scatter(data_scatter=data_drifts)

    # 显示回归结果
    st.markdown('##### 原始数据-线性回归')
    st.write(regression.summary())


def body():
    pool, kf = connection()

    # 获取数据
    if kf:
        col_1, col_2 = st.columns(2)
        with col_1:
            selected_fund = fund_selection(pool)  # 选择基金
        with col_2:
            index_data = index_selection()  # 选择指数
        get_fund_data(kf=kf, selected_fund=selected_fund)  # 获取数据

        # 显示基础信息
        basic_info(selected_fund, index_data)

        # 显示收益特征图像
        plot(fund=selected_fund, index_data=index_data)


def app():
    header()
    body()
