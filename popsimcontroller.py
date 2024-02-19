#========================================================================
#
# popsimcontroller.py - class to control a population simuation
#
# Copyright Greg King 2024
# distributed under the MIT licence (see LICENCE.TXT)
#
#========================================================================

from math import pi, cos
from popsimcalculator import *


class PopSimController:
    def __init__(self, tkRoot, timeSeriesModel):
        self.__tkRoot = tkRoot
        self.__model = timeSeriesModel
        self.__calculator = PopSimCalculator()

        # just dummy model for now
        self.__dummyPhase = 0
        self.__dummyAmplitude = 5
        self.__dummyPhaseInc = pi / 10

        # ms delay between each tick
        self.__tickDelay = 1000

        # set up model
        self.__model.reset(startYear=2024)

        # starting populations
        for speciesID in self.__calculator.getSpeciesIDList():
            self.__model.addTimeSeries(speciesID)
            self.__model.setSeriesValue(speciesID, 0)

        # set up state variables
        self.__stateSubscribers = []
        self.__playing = False
        self.__resetOnTick = False

    def tick(self):
        if self.__resetOnTick:
            self.resetSim()
            self.__resetOnTick = False
        elif self.__playing:
            self.__dummyPhase += self.__dummyPhaseInc
            prevYear = self.__model.getCurrentYear()
            prevYearPopulations = self.__model.getCurrentValues()

            newYearPopulations = self.__calculator.doSimulation(prevYearPopulations)

            self.__model.advanceYear()
            self.__model.setCurrentValues(newYearPopulations)

            # for seriesID in self.__model.getSeriesIDList():
            #     prevPop = self.__model.getSeriesValue(seriesID, prevYear)
            #     newPop = int(prevPop + cos(self.__dummyPhase)*self.__dummyAmplitude)
            #     if newPop < 0:
            #         newPop = 0
            #     self.__model.setSeriesValue(seriesID, newPop)

            self.__tkRoot.after(self.__tickDelay, lambda: self.tick())

    def setSimRate(self, rate):
        self.__tickDelay = int(1000 / pow((rate+1), 2))

    def startSim(self):
        if not self.__playing:
            self.__playing = True
            self.__informStateSubscribers()
            self.tick()

    def resetSim(self):
        if self.__playing:
            self.__resetOnTick = True
        else:
            # stash initial values
            startYear = self.__model.getStartYear()
            initialValues = {}
            for seriesID in self.__model.getSeriesIDList():
                initialValues[seriesID] = self.__model.getSeriesValue(seriesID, startYear)

            self.__model.erase(startYear=2024)

            # restore initial values
            for seriesID, value in initialValues.items():
                self.__model.setSeriesValue(seriesID, value)

        self.__playing = False
        self.__informStateSubscribers()

    def pauseUnpauseSim(self):
        self.__playing = not self.__playing
        self.__informStateSubscribers()
        if self.__playing:
            self.tick()

    def overrideSeriesValue(self, seriesID, newValue):
        self.__model.setSeriesValue(seriesID, newValue)

    def subscribeToStateChanges(self, subscriber):
        self.__stateSubscribers.append(subscriber)

    def __informStateSubscribers(self):
        for subscriber in self.__stateSubscribers:
            subscriber.simStateChanged({"Playing": self.__playing})