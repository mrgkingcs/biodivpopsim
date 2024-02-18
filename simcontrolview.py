# ========================================================================
#
# simcontrolview.py - class to handle stop/start/etc. controls
#
# Copyright Greg King 2024
# distributed under the MIT licence (see LICENCE.TXT)
#
# ========================================================================

import tkinter as tk
from tkinter import ttk
import webbrowser
from os import path

from baseview import BaseView


class SimControlView(BaseView):
    PADDING = 2
    FONT = ('Arial', 14)

    def __init__(self, tkRoot, model, controller):
        super().__init__(tkRoot)

        # connect to other app components
        self.__model = model
        self.__controller = controller

        # configure the grid layout
        for column in range(3):
            self.getWidget().columnconfigure(column, weight=1)

        for row in range(3):
            self.getWidget().rowconfigure(row, weight=1)

        # add the rate slider widgets
        slowLabel = tk.Label(self.getWidget(), text="Slow",
                             padx=SimControlView.PADDING, pady=SimControlView.PADDING,
                             font=SimControlView.FONT)
        slowLabel.grid(row=0, column=0, stick='NEWS')

        fastLabel = tk.Label(self.getWidget(), text="Fast",
                             padx=SimControlView.PADDING, pady=SimControlView.PADDING,
                             font=SimControlView.FONT)
        fastLabel.grid(row=0, column=2, stick='NEWS')

        self.__rateSliderVar = tk.IntVar()
        self.__rateSlider = ttk.Scale(self.getWidget(),
                                      from_=0, to=4,
                                      variable=self.__rateSliderVar,
                                      command=lambda event: self.rateSliderChanged())
        self.__rateSlider.grid(row=1, column=0, columnspan=3, stick='EW')

        # add the current year widgets
        yearLabel = tk.Label(self.getWidget(), text="Year:", justify=tk.RIGHT,
                             padx=SimControlView.PADDING, pady=SimControlView.PADDING,
                             font=SimControlView.FONT)
        yearLabel.grid(row=2, column=0, columnspan=2, stick='NEWS')

        self.__yearValueVar = tk.StringVar()
        yearValueLabel = tk.Label(self.getWidget(), textvariable=self.__yearValueVar,
                                  justify=tk.CENTER,
                                  padx=SimControlView.PADDING, pady=SimControlView.PADDING,
                                  font=SimControlView.FONT)
        yearValueLabel.grid(row=2, column=2, stick='NEWS')

        # add the sim controls buttons
        baseIconPath = path.join(path.dirname(__file__), "icons")
        self.__resetIcon = tk.PhotoImage(file=path.join(baseIconPath, "icons8-restart-64.png"))
        resetButton = tk.Button(self.getWidget(), text="Reset",
                                image=self.__resetIcon,
                                compound=tk.TOP,
                                command=lambda: self.resetSim())
        resetButton.grid(row=3, column=0, stick='NEWS')

        self.__playIcon = tk.PhotoImage(file=path.join(baseIconPath, "icons8-circled-play-64.png"))
        self.__playButton = tk.Button(self.getWidget(), text="Start",
                                      image=self.__playIcon,
                                      compound=tk.TOP,
                                      command=lambda: self.startSim())
        self.__playButton.grid(row=3, column=1, stick='NEWS')

        self.__pauseIcon = tk.PhotoImage(file=path.join(baseIconPath, "icons8-pause-button-64.png"))
        self.__pauseButton = tk.Button(self.getWidget(), text="Pause",
                                       image=self.__pauseIcon,
                                       compound=tk.TOP,
                                       state='disabled',
                                       command=lambda: self.pauseSim())
        self.__pauseButton.grid(row=3, column=2, stick='NEWS')

        # add the required licencing link to icons8.com
        licenceLabel = tk.Label(self.getWidget(), text="Icons by icons8.com", justify=tk.CENTER,
                                padx=SimControlView.PADDING, pady=SimControlView.PADDING,
                                fg='blue', cursor="hand2")
        licenceLabel.bind("<Button-1>", lambda e: webbrowser.open_new("https://icons8.com"))
        licenceLabel.grid(row=4, column=0, columnspan=4, stick='NEWS')

        # subscribe to state changes
        self.__controller.subscribeToStateChanges(self)

        # subscribe to year changes
        self.__model.subscribeToYearChange(self)

        # for layout debug
        self.getWidget().config(bg='yellow')
        # label = tk.Label(self.getWidget(), text="SimControlView")
        # label.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)

    def simStateChanged(self, newStateInfo):
        if newStateInfo["Playing"]:
            self.__playButton.config(state='disabled')
            self.__pauseButton.config(state='normal')
        else:
            self.__playButton.config(state='normal')
            self.__pauseButton.config(state='disabled')

    def rateSliderChanged(self):
        self.__controller.setSimRate(self.__rateSliderVar.get())

    def yearsUpdated(self, yearData):
        self.__yearValueVar.set(str(yearData["endYear"]))

    def resetSim(self):
        self.__controller.resetSim()

    def startSim(self):
        self.__controller.startSim()

    def pauseSim(self):
        self.__controller.pauseUnpauseSim()
