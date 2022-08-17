"""
基金评价页
"""

import streamlit as st

from yz_finance.utility.multi_page import MultiPage
from yz_finance.utility.streamlit_template import template_header, sub_page_selection
from pages.Fund_evaluation_subpages import basic_evaluation, CAPM


def header():
    template_header()
    st.subheader('基金评价')


def sidebar():
    pass


def body():
    pages = {'基金基础评价': basic_evaluation.app,
             'CAPM': CAPM.app}
    sub_page_selection(pages=pages)


if __name__ == '__main__':
    header()
    sidebar()
    body()
