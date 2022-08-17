"""
data_update
"""

import streamlit as st

from yz_finance.utility.multi_page import MultiPage
from yz_finance.utility.streamlit_template import template_header
from pages.Data_download_subpages import update, single_fund_download_kingfund, indexes_weekly


def body():
    st.header('数据更新页')
    # sub_page
    sub_page = MultiPage()
    sub_page.add_app("工具数据更新", update.app)
    sub_page.add_app("私募基金数据下载", single_fund_download_kingfund.app)
    sub_page.add_app("周报指数数据", indexes_weekly.app)

    sub_page.run()


if __name__ == '__main__':
    template_header()
    body()
