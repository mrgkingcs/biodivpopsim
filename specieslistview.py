#========================================================================
#
# specieslistview.py - class to display a list of species and populations
#
# Copyright Greg King 2024
# distributed under the MIT licence (see LICENCE.TXT)
#
#========================================================================

import tkinter as tk

from baseview import BaseView


class SpeciesListView(BaseView):
    def __init__(self, tkRoot, model, controller):
        super().__init__(tkRoot)
        self.__model = model
        self.__controller = controller

        # for layout debug
        self.getWidget().config(bg='yellow')
        label = tk.Label(self.getWidget(), text="SpeciesListView")
        label.grid(row=0, column=0, sticky=tk.N+tk.E+tk.S+tk.W)

