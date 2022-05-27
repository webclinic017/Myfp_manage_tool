"""
data_update
"""

import streamlit as st

from Support.Multipage import MultiPage
from Pages.Data_download_subpages import update, single_fund_download_kingfund, indexes_weekly


def header():
    st.write('---')
    st.subheader('数据更新页')


def sidebar():
    pass


def body():
    # sub_page
    sub_page = MultiPage()
    sub_page.add_app("工具数据更新", update.app)
    sub_page.add_app("私募基金数据下载", single_fund_download_kingfund.app)
    sub_page.add_app("周报指数数据", indexes_weekly.app)

    sub_page.run()


def app():
    header()
    sidebar()
    body()

    # # 实例化kingfund模块
    # kf = KingFund.KingFund()
    #
    # def update_data():
    #     # 数据更新部分
    #     def update_index():
    #         pass
    #
    #     def update_private_fund():
    #         pass
    #
    #     def update_mutual_fund():
    #         pass
    #
    #     col1, col2, col3 = st.columns((7, 1.5, 1.5))
    #
    #     with col1:
    #         # 显示最新数据
    #         index_last_date, private_last_date, mutual_last_date = '待修改', '待修改', '待修改'
    #         st.write(f'最新指数-数据日期: {index_last_date}')
    #         st.write(f'最新私募-数据日期: {private_last_date}')
    #         st.write(f'最新公募-数据日期: {mutual_last_date}')
    #
    #     with col2:
    #         update_all_button = st.button('更新全部')
    #         index_update_button = st.button('更新指数')
    #
    #         if update_all_button:
    #             update_index()
    #             update_private_fund()
    #             update_mutual_fund()
    #
    #         if index_update_button:
    #             update_index()
    #
    #     with col3:
    #         private_update_button = st.button('更新私募')
    #         mutual_update_button = st.button('更新公募')
    #
    #         if private_update_button:
    #             update_private_fund()
    #
    #         if mutual_update_button:
    #             update_mutual_fund()
    #
    # # 获取单一标的
    #
    # def get_fund_data():
    #     st.subheader('金方数据库数据下载')
    #
    #     download_fund_name = st.text_input('请输入基金名称')
    #
    #     # 获取fund_code
    #     def get_fund_code():
    #         fund_code_all = kf.get_fund_code_by_name(download_fund_name)
    #
    #         fund_name = st.selectbox(label='请选择基金', options=fund_code_all.index)
    #         fund_code = fund_code_all.loc[fund_name, 'fund_code']
    #
    #         return fund_name, fund_code, fund_code_all
    #
    #     if download_fund_name:
    #         try:
    #             selected_fund_name, selected_fund_code, fund_code_table = get_fund_code()
    #             st.table(fund_code_table)
    #
    #             update_button = st.button('获取数据')
    #
    #             if update_button:
    #                 try:
    #                     fund_data = kf.get_equity_price(fund_name=selected_fund_name, fund_code=selected_fund_code)
    #                     st.write(fund_data.tail())
    #                     st.download_button(label='保存数据',
    #                                        data=fund_data.to_csv().encode('utf-8'),
    #                                        file_name=f'{selected_fund_name}净值.csv',
    #                                        mime='text/csv')
    #                 except:
    #                     st.warning('连接失败，请重试！')
    #         except:
    #             st.warning('获取fund_code失败，请重试！')
    #
    # update_data()
    # get_fund_data()
