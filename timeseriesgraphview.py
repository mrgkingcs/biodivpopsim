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
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class TimeSeriesGraphView(BaseView):
    DPI = 72

    def __init__(self, tkRoot, model, seriesID, controller):
        super().__init__(tkRoot)
        self.__model = model
        self.__controller = controller

        self.__seriesID = seriesID
        self.__model.subscribeToSeries(seriesID, self)

        # create the canvas on which to draw the graph
        self.__graphCanvas = tk.Canvas(self.getWidget())
        self.__graphCanvas.pack(fill=tk.BOTH)

        self.getWidget().bind("<Configure>", lambda event: self.widgetResized(event))

        # create the matplotlib link
        self.__figure = Figure(dpi=TimeSeriesGraphView.DPI)
        self.__graph = FigureCanvasTkAgg(self.__figure, self.__graphCanvas)

        self.__graph.get_tk_widget().bind("<Configure>", lambda event: self.canvasResized(event))

        self.__plot = self.__figure.add_subplot(1, 1, 1)
        self.__plot.set_aspect('auto')

        self.__graph.get_tk_widget().pack()

        # for layout debug
        self.getWidget().config(bg='red')
        # label = tk.Label(self.getWidget(), text=str(seriesID))
        # label.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)

    def timeSeriesUpdated(self, seriesData):
        """Re-plot time series to canvas"""
        pass

    def canvasResized(self, event):
        print(f"Resized canvas to:{event.width},{event.height}")

    def widgetResized(self, event):
        print(f"Resizing widget to:{event.width},{event.height}")
        self.__figure.set_size_inches(event.width/TimeSeriesGraphView.DPI,
                                      event.height/TimeSeriesGraphView.DPI)
        print("Overriding canvas size")
        self.__graph.get_tk_widget().config(width=event.width, height=event.height)
        print("Calling resize on graph")
        self.__graph.resize(event)
        print("Calling draw on graph")
        self.__graph.draw()
        #self.__graph.flush_events()

