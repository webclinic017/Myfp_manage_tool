"""
池子管理会

subpages:
1. 池子概览
2. 池子业绩
"""

import streamlit as st

from Support.Multipage import MultiPage
from Pages.Pool_manage_subpages import pool_general_info, pool_perfomance


def header():
    st.write('---')
    st.subheader('池子管理页')


def sidebar():
    pass


def body():
    # sub_page
    sub_page = MultiPage()
    sub_page.add_app("池子概览", pool_general_info.app)
    sub_page.add_app("池子业绩", pool_perfomance.app)

    sub_page.run()


def app():
    header()
    sidebar()
    body()

