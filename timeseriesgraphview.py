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
        self.__plot.spines['top'].set_visible(False)
        self.__plot.spines['right'].set_visible(False)

        self.__plot.set_title(seriesID)
        self.__plot.set_xlabel("Year")
        self.__plot.set_xlim([0, 10])
        self.__plot.set_ylabel("Population")
        self.__plot.set_ylim([0, 10])

        self.__populationLine, = self.__plot.plot([0, 1], [0, 0]) # apparently plot returns a tuple

        self.__graph.get_tk_widget().pack()

        # for layout debug
        self.getWidget().config(bg='red')
        # label = tk.Label(self.getWidget(), text=str(seriesID))
        # label.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)

    def timeSeriesUpdated(self, seriesData):
        """Re-plot time series to canvas"""

        popValues = seriesData["seriesValues"]

        # calc x bounds
        startYear, endYear = seriesData["startYear"], seriesData["endYear"]
        upperXBound = endYear
        if endYear - startYear < 10:
            upperXBound = startYear + 10
        self.__plot.set_xlim([startYear, upperXBound])

        # calc y bounds
        maxPop = max(popValues)
        lowerYBound, upperYBound = self.__plot.get_ylim()
        while upperYBound < maxPop:
            upperYBound *= 10
        self.__plot.set_ylim([lowerYBound, upperYBound])

        # update the data
        self.__populationLine.set_xdata(list(range(startYear, endYear+1)))
        self.__populationLine.set_ydata(popValues)

        self.__graph.draw()
        self.__graph.flush_events()

    def canvasResized(self, event):
        #print(f"Resized canvas to:{event.width},{event.height}")
        pass

    def widgetResized(self, event):
        #print(f"Resizing widget to:{event.width},{event.height}")
        self.__figure.set_size_inches(event.width/TimeSeriesGraphView.DPI,
                                      event.height/TimeSeriesGraphView.DPI)
        #print("Overriding canvas size")
        self.__graph.get_tk_widget().config(width=event.width, height=event.height)
        #print("Calling resize on graph")
        self.__graph.resize(event)
        #print("Calling draw on graph")
        self.__graph.draw()

