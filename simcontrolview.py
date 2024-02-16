#========================================================================
#
# simcontrolview.py - class to handle stop/start/etc. controls
#
# Copyright Greg King 2024
# distributed under the MIT licence (see LICENCE.TXT)
#
#========================================================================

from baseview import BaseView


class SimControlView(BaseView):
    def __init__(self, tkRoot, model, controller):
        super().__init__(tkRoot)
        self.__model = model
        self.__controller = controller
