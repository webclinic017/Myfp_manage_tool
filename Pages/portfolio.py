"""
组合模拟
"""

import streamlit as st

from Support.Multipage import MultiPage
from Support.Matplot_CH_Font import matplot_ch_font
from Pages.Portfolio_subpages import portfolio_stimulation


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
