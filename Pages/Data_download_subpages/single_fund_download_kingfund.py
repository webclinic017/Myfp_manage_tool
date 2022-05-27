"""
data_update
"""

import streamlit as st
import pandas as pd

from Support import KingFund


def header():
    st.write('---')
    st.subheader('私募基金数据下载')


def sidebar():
    pass


def body():
    # 实例化kingfund模块
    kf = KingFund.KingFund()

    # 获取单一标的

    def get_fund_data():

        download_fund_name = st.text_input('请输入基金名称')

        # 获取fund_code
        def get_fund_code():
            fund_code_all = kf.get_fund_code_by_name(download_fund_name)

            fund_names = st.multiselect(label='请选择基金', options=fund_code_all.index)
            fund_names = list(fund_names)
            fund_codes = []

            for fund_name in fund_names:
                fund_codes.append(fund_code_all.loc[fund_name, 'fund_code'])

            return fund_names, fund_codes, fund_code_all

        # 判断输入是否为空
        if download_fund_name:
            try:
                selected_fund_names, selected_fund_codes, fund_code_table = get_fund_code()
                st.table(fund_code_table)

                col_1, col_2 = st.columns(2)
                with col_1:
                    separate_update_button = st.button('分别获取基金净值数据')

                    def data_separate():
                        for selected_fund_name, selected_fund_code in zip(selected_fund_names, selected_fund_codes):
                            try:
                                fund_data = kf.get_equity_price(fund_name=selected_fund_name,
                                                                fund_code=selected_fund_code)
                                st.write(fund_data)
                                st.download_button(label='保存数据',
                                                   data=fund_data.to_csv().encode('utf-8'),
                                                   file_name=f'{selected_fund_name}净值.csv',
                                                   mime='text/csv')
                            except:
                                st.warning('连接失败，请重试！')

                with col_2:
                    combine_update_button = st.button('获取基金合并净值数据--复权净值')

                    def data_combine():
                        all_fund_ac_data = []
                        for selected_fund_name, selected_fund_code in zip(selected_fund_names, selected_fund_codes):
                            try:
                                fund_data = kf.get_equity_price(fund_name=selected_fund_name,
                                                                fund_code=selected_fund_code)
                                all_fund_ac_data.append(fund_data.iloc[:, -1].copy())

                            except:
                                st.warning('连接失败，请重试！')

                        st.write('## 同期数据')
                        output = pd.concat(all_fund_ac_data, axis=1, join='inner')
                        output.sort_index(ascending=True, inplace=True)

                        st.write(output)
                        st.download_button(label='保存数据',
                                           data=output.to_csv().encode('utf-8'),
                                           file_name=f'合并基金复权净值.csv',
                                           mime='text/csv')

                        st.write('---')

                        st.write('## 所有数据')
                        output = pd.concat(all_fund_ac_data, axis=1)
                        output.sort_index(ascending=True, inplace=True)

                        st.write(output)
                        st.download_button(label='保存数据',
                                           data=output.to_csv().encode('utf-8'),
                                           file_name=f'合并基金复权净值.csv',
                                           mime='text/csv')

                # 分别获取基金净值数据
                if separate_update_button:
                    st.write('---')
                    data_separate()

                # 获取合并净值
                if combine_update_button:
                    st.write('---')
                    data_combine()
            except:
                st.warning('失败，请重试！')

    get_fund_data()


def app():
    header()
    sidebar()
    body()

# %%
