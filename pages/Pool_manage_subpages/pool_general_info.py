"""
池子概览页

50池各标的数量，占比，总数
"""

import streamlit as st
import pandas as pd

from yz_finance.data_get.kingfund import KingFund


def header():
    st.write('---')
    st.subheader('池子概览页')


def sidebar():
    pass


def body():
    # setting and reading
    pool_list = pd.read_excel('data/Funds list/pool.xlsx')
    pool_list.sort_values('二级策略', inplace=True, ascending=False)

    # 50池标的df
    st.subheader('50池列表')
    pool_50 = pool_list[pool_list['所属池'] == '50池'].copy()
    pool_50.reset_index(drop=True, inplace=True)
    pool_50.index = pool_50.index + 1

    # 分策略显示50池标的
    strategies = ('全部策略', '股票单边', '量化选股', '量化CTA', '市场中性', '套利策略', '事件驱动')
    strategy = st.radio('选择策略', options=strategies, horizontal=True)

    if strategy == '全部策略':
        st.write(pool_50)
    elif strategy == '股票单边':
        st.write(pool_50[pool_50['二级策略'] == '股票单边'])
    elif strategy == '量化选股':
        st.write(pool_50[pool_50['二级策略'] == '量化选股'])
    elif strategy == '量化CTA':
        st.write(pool_50[pool_50['二级策略'] == '量化CTA'])
    elif strategy == '市场中性':
        st.write(pool_50[pool_50['二级策略'] == '市场中性'])
    elif strategy == '套利策略':
        st.write(pool_50[pool_50['二级策略'] == '套利策略'])
    elif strategy == '事件驱动':
        st.write(pool_50[pool_50['二级策略'] == '事件驱动'])

    # 50池占比
    col1, col2 = st.columns(2)
    with col1:
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

    with col2:
        # 显示200池各标的比例
        pool_200 = pool_list[(pool_list['所属池'] == '200池') | (pool_list['所属池'] == '50池')].copy()

        st.write(f"""
        ####  200池基本情况（包含50池）
        200池当前标的数量：{pool_200.shape[0]}
        """
                 )

        # 显示2000池各标的比例
        pool_200_count = pool_200['二级策略'].value_counts().copy()
        pool_200_ratio = round(pool_200_count / pool_200.shape[0] * 100, 2)

        pool_200_count.name = '数量'
        pool_200_ratio.name = '比例(%)'

        pool_200_output = pd.concat([pool_200_count, pool_200_ratio], axis=1)

        st.table(pool_200_output)

    # 更新50池信息
    st.write('---')
    st.header('更新50池信息')

    col1, col2 = st.columns(2)
    # 更新信息
    with col1:

        st.subheader('更新50池内标的信息')
        with st.form('更新50池内标的信息'):
            update_fund = st.selectbox('选择标的', options=pool_50['基金名称'])
            update_name = st.text_input('更新标的名称')



            strategy = st.selectbox('更改所属策略', options=strategies[1:])
            dai_xiao = st.selectbox('更改代销状态', options=('是', '否'))
            tou_zi = st.selectbox('更改投资状态', options=('是', '否'))
            bu_ke_tou = st.text_input('不可投原因')
            bei_zhu = st.text_input('备注')

            # Every form must have a submit button.
            submitted = st.form_submit_button("提交")
            if submitted:
            # 根据输入名称获取fund_code
                if update_name:
                    try:
                        kf = KingFund()  # 实例化kingfund模块

                        def get_fund_code():
                            fund_code_all = kf.get_fund_code_by_name(update_name)

                            fund_name = st.select(label='请选择基金', options=fund_code_all.index)
                            fund_code = fund_code_all.loc[fund_name, 'fund_code']

                            return fund_code

                        update_fund_code = get_fund_code()
                        st.write(update_name, update_fund_code)
                    except:
                        kf = None
                        st.warning('无法连接至金方数据库，请在公司内网重试！')


    with col2:
        st.subheader('新增标的入池')
        with st.form('新增标的入池'):

            update_pool = pool_list[pool_list['所属池'] == '200池']
            update_fund = st.selectbox('选择标的', options=update_pool['基金名称'])

            # Every form must have a submit button.
            submitted = st.form_submit_button('入50池')
            if submitted:
                pool_list['所属池'][pool_list['基金名称'] == update_fund] = '50池'
                pool_list.to_excel('data/Funds list/pool.xlsx', index=False)

                st.write(pool_list[pool_list['基金名称'] == update_fund]['所属池'])
                st.success('更新成功!')

        st.subheader('50标的出池')
        with st.form('50标的出池'):
            update_fund = st.selectbox('选择标的', options=pool_50['基金名称'])

            # Every form must have a submit button.
            submitted = st.form_submit_button('出50池')
            if submitted:
                pool_list[pool_list['基金名称'] == update_fund]['所属池'] = '200池'
                pool_list.to_excel('data/Funds list/pool.xlsx', index=False)
                st.success('更新成功!')


def app():
    header()
    sidebar()
    body()
