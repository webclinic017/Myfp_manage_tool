"""
周报指数更新
"""

import streamlit as st
import pandas as pd
import tushare as ts


def header():
    st.write('---')
    st.subheader('指数周报数据')
    st.markdown("""
                数据来源：tushare.pro
                """)


def sidebar():
    pass


def body():
    # 指数list
    stock_index_list = {'上证指数': '000001.SH', '沪深300': '000300.SH', '中证500': '000905.SH',
                        '创业板指': '399006.SZ', '科创50': '000688.SH'}
    commodity_index_list = {'南华商品': 'NHCI.NH', '南华农产品': 'NHAI.NH', '南华能化': 'NHECI.NH',
                            '南华黑色': 'NHFI.NH', '南华工业品': 'NHII.NH', '南华金属': 'NHMI.NH',
                            '南华有色': 'NHNFI.NH', '南华贵金属': 'NHPMI.NH'}

    # 更新数据按钮
    button = st.button('更新数据')

    if button:
        with st.spinner('正在处理中...'):
            # 获取指数收盘价数据，周频
            def index_close_daily(index_name, ts_code, start_date='', end_date=''):
                pro = ts.pro_api('8048cbf9b5b32cf6c5ca12b8863a1869901b566749dccbd796b458b5')
                df = pro.index_daily(**{
                    "ts_code": ts_code,
                    "trade_date": "",
                    "start_date": start_date,
                    "end_date": end_date,
                    "limit": "",
                    "offset": ""
                }, fields=["trade_date",
                           "close"
                           ])
                df.rename(columns={'close': index_name}, inplace=True)

                df.set_index('trade_date', inplace=True)
                df.index = pd.to_datetime(df.index, format='%Y%m%d')
                df.sort_index(ascending=True, inplace=True)
                return df

            stock_index_update = map(index_close_daily, stock_index_list.keys(), stock_index_list.values())
            stock_index_update = list(stock_index_update)

            stock_index_update = pd.concat(stock_index_update, axis=1)
            stock_index_update.columns = stock_index_list.keys()
            stock_index_update.index = pd.to_datetime(stock_index_update.index).date

            commodity_index_update = map(index_close_daily, commodity_index_list.keys(), commodity_index_list.values())
            commodity_index_update = list(commodity_index_update)

            commodity_index_update = pd.concat(commodity_index_update, axis=1)
            commodity_index_update.columns = commodity_index_list.keys()
            commodity_index_update.index = pd.to_datetime(commodity_index_update.index).date

            # stock_index_update.to_csv('Apps/weekly_report/Data/stock_index_update.csv')
            # commodity_index_update.to_csv('Apps/weekly_report/Data/commodity_index_update.csv')

        # 选择指数
        st.write('___')
        st.markdown("""
                    指数数据
                    """)
        # stock_index_value = pd.read_csv('Apps/weekly_report/Data/stock_index_update.csv', index_col=0)
        # commodity_index_value = pd.read_csv('Apps/weekly_report/Data/commodity_index_update.csv', index_col=0)
        st.sidebar.subheader('股票指数日期设置')
        this_week = st.sidebar.selectbox('本周日期', options=stock_index_update.index,
                                         index=stock_index_update.shape[0] - 1)
        last_week = st.sidebar.selectbox('上周日期', options=stock_index_update.index,
                                         index=stock_index_update.shape[0] - 6)
        week_before = st.sidebar.selectbox('两周前日期', options=stock_index_update.index,
                                           index=stock_index_update.shape[0] - 11)

        st.write('股票指数')
        this_week_return = stock_index_update.loc[this_week, :] / stock_index_update.loc[last_week, :] - 1
        last_week_return = stock_index_update.loc[last_week, :] / stock_index_update.loc[week_before, :] - 1
        data = pd.concat([this_week_return, last_week_return], axis=1)
        data.columns = ['本周涨跌幅(%)', '上周涨跌幅(%)']
        st.table(data * 100)

        st.write('___')
        st.write(stock_index_update.tail(10))

        # 商品指数
        st.write('商品指数')

        st.sidebar.subheader('商品指数日期设置')
        c_this_week = st.sidebar.selectbox('本周日期',
                                           options=commodity_index_update.index,
                                           index=commodity_index_update.shape[0] - 1)
        c_last_week = st.sidebar.selectbox('上周日期',
                                           options=commodity_index_update.index,
                                           index=commodity_index_update.shape[0] - 6)
        c_week_before = st.sidebar.selectbox('两周前日期',
                                             options=commodity_index_update.index,
                                             index=commodity_index_update.shape[0] - 11)

        c_this_week_return = commodity_index_update.loc[c_this_week, :] / commodity_index_update.loc[c_last_week,
                                                                          :] - 1
        c_last_week_return = commodity_index_update.loc[c_last_week, :] / commodity_index_update.loc[c_week_before,
                                                                          :] - 1
        data = pd.concat([c_this_week_return, c_last_week_return], axis=1)
        data.columns = ['本周涨跌幅(%)', '上周涨跌幅(%)']
        st.table(data * 100)

        st.write('___')
        st.write(commodity_index_update.tail(10))


def app():
    header()
    sidebar()
    body()
