"""
Home page
"""

import streamlit as st


def header():
    st.write('---')
    st.subheader('主页')


def sidebar():
    pass


def body():
    st.markdown("""
                #### 包含工具：
                - 数据下载
                - 弘酬投资池管理
                - 弘酬产品管理工具
                    - 周报工具
                    - 月报工具
                    - 产品管理会文件工具
                - 基金评价
                """)


def app():
    header()
    sidebar()
    body()
