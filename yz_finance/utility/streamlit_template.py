"""
Main program
"""

from PIL import Image

import streamlit as st
from .multi_page import MultiPage


def template_header():
    header_col_1, header_col_2 = st.columns((6.5, 3.5))

    with header_col_1:
        # 标志
        sign_image = Image.open('data/SAMCO sign.png')
        st.image(sign_image)

    with header_col_2:
        st.markdown("""
                Author: Yanzhong Huang  
                Version: 2.0, Update: 1 May 2022  
                数据来源：金方数据库  
                """)

    st.write('---')


def sub_page_selection(pages: dict):
    # sub_page
    sub_page = MultiPage()

    for name, page in pages.items():
        sub_page.add_app(name, page)

    sub_page.run()
