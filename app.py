#========================================================================
#
# app.py - class to setup and run all the classes involved in the app
#
# Copyright Greg King 2024
# distributed under the MIT licence (see LICENCE.TXT)
#
#========================================================================

import tkinter as tk

from timeseriesmodel import TimeSeriesModel
from popsimcontroller import PopSimController
from specieslistview import SpeciesListView
from simcontrolview import SimControlView
from timeseriesgraphview import TimeSeriesGraphView

PADDING = 0
ALL_DIRS = tk.N + tk.S + tk.E + tk.W
NUM_COLUMNS_OF_GRAPHS = 4

class App:
    def __init__(self):
        self.__root = None
        self.__views = []
        self.__controller = None
        self.__model = None

    def run(self):
        self.__root = tk.Tk()
        self.__root.title("Biodiversity Population Simulator")
        self.__root.config(bg='blue')

        self.setupModel()
        self.setupController()
        self.setupViews()

        self.__root.mainloop()

    def setupModel(self):
        self.__model = TimeSeriesModel()

        #just dummy model for now
        for count in range(10):
            self.__model.addTimeSeries("DummySeries"+str(count+1))

    def setupController(self):
        self.__controller = PopSimController(self.__model)

    def setupViews(self):
        speciesListView = SpeciesListView(self.__root, self.__model, self.__controller)
        speciesListView.getWidget().grid(row=0, column=5, rowspan=2, padx=PADDING, pady=PADDING, sticky=ALL_DIRS)
        self.__views.append(speciesListView)

        simControlView = SimControlView(self.__root, self.__model, self.__controller)
        simControlView.getWidget().grid(row=2, column=5, padx=PADDING, pady=PADDING, sticky=ALL_DIRS)
        self.__views.append(simControlView)

        seriesCounter = 0
        for seriesID in self.__model.getSeriesIDList():
            timeSeriesView = TimeSeriesGraphView(self.__root, self.__model, seriesID, self.__controller)
            graphRow = int(seriesCounter / NUM_COLUMNS_OF_GRAPHS)
            graphColumn = seriesCounter % NUM_COLUMNS_OF_GRAPHS
            timeSeriesView.getWidget().grid(row=graphRow, column=graphColumn, padx=PADDING, pady=PADDING, sticky=ALL_DIRS)
            self.__views.append(timeSeriesView)
            seriesCounter += 1

        maxRow = int(seriesCounter / NUM_COLUMNS_OF_GRAPHS)
        for idx in range(maxRow+1):
            self.__root.rowconfigure(idx, weight=1)
        for idx in range(NUM_COLUMNS_OF_GRAPHS+1):
            self.__root.columnconfigure(idx, weight=1)


if __name__ == "__main__":
    app = App()
    app.run()