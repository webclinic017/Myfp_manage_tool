import streamlit as st
import pandas as pd
import numpy as np

from yz_finance.data_get.kingfund import KingFund
from yz_finance.data_objective.fund_class import Fund
from yz_finance.calculation.basic import BasicCalculation
from yz_finance.data_get.tushare_pro import TushareData

ts = TushareData()


def header():
    st.write('---')
    st.subheader('基础评价')


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


# 净值曲线，回撤曲线
def plot(selected_fund, index_data):
    st.subheader('区间表现')
    # 选择时间段
    col_1, col_2 = st.columns(2)
    with col_1:
        start = st.date_input(label='起始日期',
                              value=selected_fund.prices_data.index[0],
                              min_value=selected_fund.prices_data.index[0],
                              max_value=selected_fund.prices_data.index[-1])

    with col_2:
        end = st.date_input(label='结束日期',
                            value=selected_fund.prices_data.index[-1],
                            min_value=selected_fund.prices_data.index[0],
                            max_value=selected_fund.prices_data.index[-1])

    # 选取对应时间段数据
    data = pd.concat([selected_fund.prices_data.iloc[:, 2], index_data], axis=1, join='inner')
    data = data[start:end]
    # 区间收益、波动
    st.write('区间表现')
    accumulate = BasicCalculation.accumulate_return_linear(data)

    duration_return = (accumulate.iloc[-1, :] - 1) * 100
    duration_return.name = '区间收益%'

    duration_vol = BasicCalculation.volatility_linear(data) * np.sqrt(52) * 100
    duration_vol.name = '区间年化波动率%'

    output = pd.concat([duration_return,duration_vol], axis=1, join='inner')
    st.table(output)
    # 收益曲线
    st.write('区间累计收益曲线')
    st.line_chart(accumulate)
    # 波动曲线
    st.write('区间滚动波动曲线')
    rolling_vol = BasicCalculation.rolling_volatility_linear(data)
    st.line_chart(rolling_vol)
    # 回撤曲线
    # st.line_chart()


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

        # 显示结果
        basic_info(selected_fund, index_data)
        plot(selected_fund, index_data)


def app():
    header()
    body()
