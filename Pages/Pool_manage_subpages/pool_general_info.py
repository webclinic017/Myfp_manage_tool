"""
池子概览页

50池各标的数量，占比，总数
"""

import streamlit as st
import pandas as pd


def header():
    st.write('---')
    st.subheader('池子概览页')


def sidebar():
    pass


def body():
    # setting and reading
    pool_list = pd.read_excel('Data/Funds list/pool.xlsx')

    #
    pool_50 = pool_list[pool_list['所属池'] == '50池']

    st.write(f"""
    ####  50池基本情况
    50池当前标的数量：{pool_50.shape[0]}
    """
             )

    # 显示50池各标的比例
    pool_50_count = pool_50['二级策略'].value_counts().copy()
    pool_50_ratio = round(pool_50_count / pool_50.shape[0] * 100, 2)

    pool_50_count.name = '数量'
    pool_50_ratio.name = '比例(%)'

    pool_50_output = pd.concat([pool_50_count, pool_50_ratio], axis=1)

    st.table(pool_50_output)

    # 显示200池各标的比例
    pool_200 = pool_list[(pool_list['所属池'] == '200池') | (pool_list['所属池'] == '50池')]

    st.write(f"""
    ####  200池基本情况（包含50池）
    200池当前标的数量：{pool_200.shape[0]}
    """
             )

    # 显示50池各标的比例
    pool_200_count = pool_200['二级策略'].value_counts().copy()
    pool_200_ratio = round(pool_200_count / pool_200.shape[0] * 100, 2)

    pool_200_count.name = '数量'
    pool_200_ratio.name = '比例(%)'

    pool_200_output = pd.concat([pool_200_count, pool_200_ratio], axis=1)

    st.table(pool_200_output)



def app():
    header()
    sidebar()
    body()
