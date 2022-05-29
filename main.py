"""
Main program
"""

from PIL import Image

import streamlit as st

from Support.Multipage import MultiPage
from Pages import home, data_update, pool_manage, product_manage, fund_evaluation, portfolio


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
    app.add_app("数据下载", data_update.app)
    app.add_app("投资池管理", pool_manage.app)
    app.add_app("产品管理", product_manage.app)
    app.add_app("基金评价", fund_evaluation.app)
    app.add_app("组合模拟", portfolio.app)

    # The main app
    app.run()


def myfp_app_run():
    header()
    body()


if __name__ == '__main__':
    myfp_app_run()
