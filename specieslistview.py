#========================================================================
#
# specieslistview.py - class to display a list of species and populations
#
# Copyright Greg King 2024
# distributed under the MIT licence (see LICENCE.TXT)
#
#========================================================================

from baseview import BaseView


class SpeciesListView(BaseView):
    def __init__(self, tkRoot, model, controller):
        super().__init__(tkRoot)
        self.__model = model
        self.__controller = controller

        # debug for layout
        self.getWidget().configure(background="blue")

