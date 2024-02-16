#========================================================================
#
# baseview.py - parent class for any view to provide common functionality
#
# Copyright Greg King 2024
# distributed under the MIT licence (see LICENCE.TXT)
#
#========================================================================

import tkinter as tk


class BaseView:
    def __init__(self, tkRoot):
        self.__widget = tk.Frame(tkRoot)

    def getWidget(self):
        return self.__widget

    def timeSeriesUpdated(self, seriesData):
        pass
