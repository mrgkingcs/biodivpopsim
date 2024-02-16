#========================================================================
#
# timeseriesgraphview.py - class to show a timeseries graph
#
# Copyright Greg King 2024
# distributed under the MIT licence (see LICENCE.TXT)
#
#========================================================================

import tkinter as tk

from baseview import BaseView


class TimeSeriesGraphView(BaseView):
    def __init__(self, tkRoot, model, seriesID, controller):
        super().__init__(tkRoot)
        self.__model = model
        self.__controller = controller

        self.__seriesID = seriesID
        self.__model.subscribeToSeries(seriesID, self)

        # for layout debug
        self.getWidget().config(bg='red')
        label = tk.Label(self.getWidget(), text=str(seriesID))
        label.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)

