"""
池子业绩
"""

import streamlit as st
import pandas as pd
import datetime

from yz_finance.data_get.kingfund import KingFund
from yz_finance.data_objective.fund_class import Fund
from yz_finance.data_get.tushare_pro import TushareData
from yz_finance.calculation.basic import BasicCalculation
from yz_finance.calculation.regression import Regression

ts = TushareData()


def header():
    st.write('---')
    st.subheader('量化策略研究')


def load_data():
    pool_list = pd.read_excel('data/Funds list/pool.xlsx')
    liang_hua = pool_list.loc[pool_list['二级策略'] == '量化选股'].copy()
    zhong_xing = pool_list.loc[pool_list['二级策略'] == '市场中性'].copy()
    return liang_hua, zhong_xing


def pool_selection():
    pool_options = ('全部', '50池', '200池')
    pool = st.radio('选择池子', options=pool_options, horizontal=True)
    return pool


def show_fund_list(liang_hua, zhong_xing, pool):
    st.write('---')
    st.markdown('#### 池子内量化策略标的')
    st.write('量化选股策略')

    if pool == '全部':
        st.write(liang_hua)
    elif pool == '50池':
        st.write(liang_hua.loc[liang_hua['所属池'] == '50池'])
    elif pool == '200池':
        st.write(liang_hua.loc[liang_hua['所属池'] == '200池'])

    st.write('市场中性策略')

    if pool == '全部':
        st.write(zhong_xing)
    elif pool == '50池':
        st.write(zhong_xing.loc[zhong_xing['所属池'] == '50池'])
    elif pool == '200池':
        st.write(zhong_xing.loc[zhong_xing['所属池'] == '200池'])


def function_selection():
    st.write('---')
    st.markdown('#### 功能选择')
    function_options = ('基础业绩表现', 'CAPM')
    selected = st.radio('功能选择', options=function_options, horizontal=True)
    return selected


def fund_data_get(liang_hua, zhong_xing):
    # 链接金方数据库
    try:
        kf = KingFund()  # 实例化kingfund模块
    except:
        kf = None
        st.warning('无法连接至金方数据库，请在公司内网重试！')

    # 生成fund_class
    if kf:
        liang_hua_list = []
        liang_hua_data_list = []
        for fund_code in liang_hua['fund_code']:
            # 创建object
            locals()['fund_' + str(fund_code)] = \
                Fund(fund_name=liang_hua.loc[liang_hua['fund_code'] == fund_code, '基金公司'].values[0],
                     company=liang_hua.loc[liang_hua['fund_code'] == fund_code, '基金公司'].values[0],
                     fund_code=liang_hua.loc[liang_hua['fund_code'] == fund_code, 'fund_code'].values[0],
                     reg_num=liang_hua.loc[liang_hua['fund_code'] == fund_code, '备案编号'].values[0],
                     strategy=liang_hua.loc[liang_hua['fund_code'] == fund_code, '二级策略'].values[0],
                     pool=liang_hua.loc[liang_hua['fund_code'] == fund_code, '所属池'].values[0],
                     prices_data=kf.get_equity_price(
                         fund_name=liang_hua.loc[liang_hua['fund_code'] == fund_code, '基金名称'].values[0],
                         fund_code=liang_hua.loc[liang_hua['fund_code'] == fund_code, 'fund_code'].values[0])
                     )

            liang_hua_list.append(locals()['fund_' + str(fund_code)])
            # 单独提取数据
            liang_hua_data_list.append(locals()['fund_' + str(fund_code)].prices_data.iloc[:, 2])

        zhong_xing_list = []
        zhong_xing_data_list = []
        for fund_code in zhong_xing['fund_code']:
            locals()['fund_' + str(fund_code)] = \
                Fund(fund_name=zhong_xing.loc[zhong_xing['fund_code'] == fund_code, '基金名称'].values[0],
                     company=zhong_xing.loc[zhong_xing['fund_code'] == fund_code, '基金公司'].values[0],
                     fund_code=zhong_xing.loc[zhong_xing['fund_code'] == fund_code, 'fund_code'].values[0],
                     reg_num=zhong_xing.loc[zhong_xing['fund_code'] == fund_code, '备案编号'].values[0],
                     strategy=zhong_xing.loc[zhong_xing['fund_code'] == fund_code, '二级策略'].values[0],
                     pool=zhong_xing.loc[zhong_xing['fund_code'] == fund_code, '所属池'].values[0],
                     prices_data=kf.get_equity_price(
                         fund_name=zhong_xing.loc[zhong_xing['fund_code'] == fund_code, '基金名称'].values[0],
                         fund_code=zhong_xing.loc[zhong_xing['fund_code'] == fund_code, 'fund_code'].values[0])
                     )
            zhong_xing_list.append(locals()['fund_' + str(fund_code)])
            # 单独提取数据
            zhong_xing_data_list.append(locals()['fund_' + str(fund_code)].prices_data.iloc[:, 2])

        # 合并净值数据在一个表
        liang_hua_data = pd.concat(liang_hua_data_list, axis=1, join='outer')
        zhong_xing_data = pd.concat(zhong_xing_data_list, axis=1, join='outer')

        liang_hua_data.columns = [_[:-4] for _ in liang_hua_data.columns]
        zhong_xing_data.columns = [_[:-4] for _ in zhong_xing_data.columns]

        liang_hua_data.index = pd.to_datetime(liang_hua_data.index).date
        zhong_xing_data.index = pd.to_datetime(zhong_xing_data.index).date

        liang_hua_data.sort_index(ascending=True, inplace=True)
        zhong_xing_data.sort_index(ascending=True, inplace=True)

        liang_hua_data.dropna(axis=0, how='any', thresh=14, inplace=True)
        zhong_xing_data.dropna(axis=0, how='any', thresh=14, inplace=True)

        return liang_hua_list, zhong_xing_list, liang_hua_data, zhong_xing_data

    else:
        return None, None, None, None


def fund_performance(liang_hua_data, zhong_xing_data, pool):
    """
    - 周度业绩
    - 4周业绩
    - 今年以来
    """

    # 周度业绩、4周业绩、今年以来
    st.markdown(f"""
    #### 量化选股周度业绩  
    最新净值日期：{liang_hua_data.index[-1]}
    """)
    last_week_liang_hua = (liang_hua_data.iloc[-1, :] / liang_hua_data.iloc[-2, :] - 1) * 100
    four_week_liang_hua = (liang_hua_data.iloc[-1, :] / liang_hua_data.iloc[-5, :] - 1) * 100
    this_year_liang_hua = \
        (liang_hua_data.iloc[-1, :] / liang_hua_data.loc[datetime.date(2021, 12, 31), :] - 1) * 100

    output = pd.concat([last_week_liang_hua, four_week_liang_hua, this_year_liang_hua], axis=1)
    output.columns = ['本周收益%', '4周收益%', '今年以来%']
    st.table(output)

    st.markdown(f"""
    #### 中性策略周度业绩  
    最新净值日期：{zhong_xing_data.index[-1]}
    """)
    last_week_zhong_xing = (zhong_xing_data.iloc[-1, :] / zhong_xing_data.iloc[-2, :] - 1) * 100
    four_week_zhong_xing = (zhong_xing_data.iloc[-1, :] / zhong_xing_data.iloc[-5, :] - 1) * 100
    this_year_zhong_xing = \
        (zhong_xing_data.iloc[-1, :] / zhong_xing_data.loc[datetime.date(2021, 12, 31), :] - 1) * 100

    output_2 = pd.concat([last_week_zhong_xing, four_week_zhong_xing, this_year_zhong_xing], axis=1)
    output_2.columns = ['本周收益%', '4周收益%', '今年以来%']
    st.table(output_2)


def fund_CAPM(liang_hua_data, zhong_xing_data, pool):
    """
    成立以来alpha beta
    52周alpha beta
    """

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

    index_data = index_selection()

    # index_data_slice = index_data.loc[index_data.index.isin(liang_hua_data.index)]
    # index_data_slice.sort_index(ascending=True, inplace=True)

    # liang_hua_data_drifts = BasicCalculation.drifts_linear(liang_hua_data)
    # index_data_drifts = BasicCalculation.drifts_linear(index_data_slice)

    data = pd.concat([liang_hua_data, index_data], axis=1, join='inner')
    data_drifts = BasicCalculation.drifts_linear(data)
    result = []
    for column in data_drifts.columns:
        try:
            reg = Regression.OLS(y_input=data_drifts[column], x_input=data_drifts.iloc[:, -1])
            result.append((column, reg.params[0], reg.params[1]))
        except:
            continue

    # st.write(data_drifts)
    result = pd.DataFrame(result)
    result.columns = ['基金名称', 'CAPM alpha', 'CAPM beta']
    result.set_index('基金名称', drop=True, inplace=True)
    st.write(result)


def body():
    liang_hua, zhong_xing = load_data()
    pool = pool_selection()
    show_fund_list(liang_hua=liang_hua, zhong_xing=zhong_xing, pool=pool)
    # 获取数据
    liang_hua_list, zhong_xing_list, liang_hua_data, zhong_xing_data = \
        fund_data_get(liang_hua=liang_hua, zhong_xing=zhong_xing)

    # 主要功能
    selected_function = function_selection()
    if selected_function == '基础业绩表现':
        fund_performance(liang_hua_data=liang_hua_data, zhong_xing_data=zhong_xing_data, pool=pool)
    if selected_function == 'CAPM':
        fund_CAPM(liang_hua_data=liang_hua_data, zhong_xing_data=zhong_xing_data, pool=pool)


def app():
    header()
    body()
