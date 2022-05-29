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

