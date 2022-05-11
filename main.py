"""
Main program
"""

from PIL import Image

import streamlit as st

from Support.Multipage import MultiPage
from Pages import home, data_update


def header():
    header_col_1, header_col_2 = st.columns((6.5, 3.5))

    with header_col_1:
        # 标志
        sign_image = Image.open('Data/SAMCO sign.png')
        st.image(sign_image)

    with header_col_2:
        st.markdown("""
                Author: Yanzhong Huang  
                Version: 2.0, Update: 1 May 2022  
                数据来源：金方数据库  
                """)


def body():
    st.header('工具合集-导航')
    app = MultiPage()

    # Add all your application here
    app.add_app("主页", home.app)
    app.add_app("数据更新页", data_update.app)

    # The main app
    app.run()


def myfp_app_run():
    header()
    body()


if __name__ == '__main__':
    myfp_app_run()
