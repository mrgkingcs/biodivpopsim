# ========================================================================
#
# specieslistview.py - class to display a list of species and populations
#
# Copyright Greg King 2024
# distributed under the MIT licence (see LICENCE.TXT)
#
# ========================================================================

import tkinter as tk

from baseview import BaseView


class SpeciesListView(BaseView):
    PADDING = 2
    FONT = ('Arial', 12)

    def __init__(self, tkRoot, model, controller):
        super().__init__(tkRoot)
        self.__textBoxes = {}

        self.__model = model
        self.__controller = controller

        # for layout debug
        # self.getWidget().config(bg='yellow')
        # label = tk.Label(self.getWidget(), text="SpeciesListView")
        # label.grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.E+tk.S+tk.W)
        # label.config(font=('Arial', 14))

        # actual widget layout
        self.getWidget().columnconfigure(0, weight=1)
        self.getWidget().columnconfigure(1, weight=1)

        rowCount = 0
        for seriesID in self.__model.getSeriesIDList():
            label = tk.Label(self.getWidget(), text=seriesID,
                             font=SpeciesListView.FONT,
                             padx=SpeciesListView.PADDING, pady=SpeciesListView.PADDING)
            label.grid(row=rowCount, column=0, sticky='NEWS')

            textBox = tk.Entry(self.getWidget(), width=5,
                               justify='center',
                               validate="focusout",
                               validatecommand=lambda seriesID=seriesID: self.__overrideSeriesValue(seriesID),
                               font=SpeciesListView.FONT)
            textBox.bind("<Return>", lambda e: self.getWidget().focus())
            textBox.grid(row=rowCount, column=1, sticky='EW',
                         padx=SpeciesListView.PADDING,
                         pady=SpeciesListView.PADDING)
            self.__textBoxes[seriesID] = textBox

            self.getWidget().rowconfigure(rowCount, weight=1)
            rowCount += 1

        # subscribe to state changes
        self.__controller.subscribeToStateChanges(self)

        # subscribe to time series changes
        self.__model.subscribeToAllSeries(self)

    def timeSeriesUpdated(self, seriesData):
        seriesID = seriesData["seriesID"]
        if seriesID in self.__textBoxes.keys():
            # get new value (if one is there)
            newValue = 0
            seriesValues = seriesData["seriesValues"]
            if len(seriesValues) > 0:
                newValue = seriesValues[-1]

            # update text box
            textBox = self.__textBoxes[seriesID]
            prevState = textBox.cget('state')
            textBox.config(state='normal')
            textBox.delete(0, tk.END)
            textBox.insert(0, str(newValue))
            textBox.config(state=prevState)

    def simStateChanged(self, newStateInfo):
        newTextBoxState = 'normal'
        if newStateInfo["Playing"]:
            newTextBoxState = 'readonly'

        for textBox in self.__textBoxes.values():
            textBox.config(state=newTextBoxState)

    def __overrideSeriesValue(self, seriesID):
        textBox = self.__textBoxes[seriesID]
        stringValue = textBox.get()
        try:
            intValue = int(stringValue)
            if intValue >= 0:
                #print(f"Overriding {seriesID} with {intValue}")
                self.__controller.overrideSeriesValue(seriesID, intValue)
        except ValueError:
            textBox.delete(0, tk.END)

        return True
