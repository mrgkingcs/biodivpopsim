#========================================================================
#
# popsimcalculator.py - class to actually calculate the sim populations
#
# Copyright Greg King 2024
# distributed under the MIT licence (see LICENCE.TXT)
#
#========================================================================

OSPREY = "Osprey"
HERON = "Heron"
MOSQUITO = "Mosquito"
MAYFLY = "Mayfly"
FROG = "Frog"
TROUT = "Trout"
OTTER = "Otter"
ALGAE = "Algae"
MUSSELS = "Mussels"
CATFISH = "Catfish"

PREDATORS = "Predators"
PREY = "Prey"

FOOD_WEB_GRAPH = {
    OSPREY: {
        PREDATORS: [],
        PREY: [TROUT]
    },
    HERON: {
        PREDATORS: [],
        PREY: [TROUT, FROG]
    },
    MOSQUITO: {
        PREDATORS: [FROG, TROUT],
        PREY: []
    },
    MAYFLY: {
        PREDATORS: [FROG, TROUT],
        PREY: [ALGAE]
    },
    FROG: {
        PREDATORS: [HERON, OTTER],
        PREY: [MOSQUITO, MAYFLY]
    },
    TROUT: {
        PREDATORS: [HERON, OTTER, OSPREY],
        PREY: [MAYFLY, MOSQUITO]
    },
    OTTER: {
        PREDATORS: [],
        PREY: [FROG, TROUT, MUSSELS]
    },
    ALGAE: {
        PREDATORS: [CATFISH, MAYFLY, MUSSELS],
        PREY: []
    },
    MUSSELS: {
        PREDATORS: [OTTER],
        PREY: [ALGAE]
    },
    CATFISH: {
        PREDATORS: [],
        PREY: [ALGAE]
    }
}

class PopSimCalculator:
    def __init__(self):
        pass

    def getSpeciesIDList(self):
        return list(FOOD_WEB_GRAPH.keys())

    def doSimulation(self, prevYearPopulations):
        return prevYearPopulations