"""
将app分为几份，提升运行效率
"""

import streamlit as st


class MultiPage:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        # make radio horizontal
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        # app = st.sidebar.radio(
        app = st.radio(
            '导航',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()
