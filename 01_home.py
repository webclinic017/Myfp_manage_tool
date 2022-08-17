"""
home page
"""

import streamlit as st

# import yz_finance as yf
from yz_finance.utility.streamlit_template import template_header, sub_page_selection


def body():
    st.header('主页')
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


if __name__ == '__main__':
    st.set_page_config(page_title='弘酬投资工具合集', layout='wide')
    template_header()
    body()

