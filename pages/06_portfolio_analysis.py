"""
组合模拟
"""

import streamlit as st

from yz_finance.utility.multi_page import MultiPage
from yz_finance.utility.matplotlib_ch_font import matplot_ch_font
from pages.Portfolio_subpages import portfolio_stimulation


def header():
    st.write('---')
    st.subheader('数据更新页')

    matplot_ch_font()  # 设置中文字体


def sidebar():
    pass


def body():

    # sub_page
    sub_page = MultiPage()
    sub_page.add_app("工具数据更新", portfolio_stimulation.app)

    sub_page.run()


def app():
    header()
    sidebar()
    body()
