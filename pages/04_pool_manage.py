"""
池子管理会

subpages:
1. 池子概览
2. 池子业绩
"""

import streamlit as st

from yz_finance.utility.streamlit_template import template_header, sub_page_selection
from pages.Pool_manage_subpages import pool_general_info, pool_perfomance, quant_evaluation


def header():
    template_header()
    st.subheader('池子管理')


def body():
    pages = {"池子概览": pool_general_info.app,
             "池子业绩": pool_perfomance.app,
             "量化策略研究": quant_evaluation.app}

    sub_page_selection(pages=pages)


if __name__ == '__main__':
    header()
    body()
