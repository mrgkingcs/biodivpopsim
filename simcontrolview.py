#========================================================================
#
# simcontrolview.py - class to handle stop/start/etc. controls
#
# Copyright Greg King 2024
# distributed under the MIT licence (see LICENCE.TXT)
#
#========================================================================

import tkinter as tk
from baseview import BaseView


class SimControlView(BaseView):
    def __init__(self, tkRoot, model, controller):
        super().__init__(tkRoot)
        self.__model = model
        self.__controller = controller

        # for layout debug
        self.getWidget().config(bg='yellow')
        label = tk.Label(self.getWidget(), text="SimControlView")
        label.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)