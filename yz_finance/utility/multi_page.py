"""
Splits App to multiple page, in order to increase efficiency
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

        app = st.radio(
            'Navigation',
            self.apps,
            format_func=lambda app: app['title'],
            horizontal=True)

        app['function']()
