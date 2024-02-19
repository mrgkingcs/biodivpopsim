#========================================================================
#
# popsimcalculator.py - class to actually calculate the sim populations
#
# Copyright Greg King 2024
# distributed under the MIT licence (see LICENCE.TXT)
#
#========================================================================

from random import uniform

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

REQUIRED_BIOMASS_FACTOR = "Required Biomass for healthy consumption (as proportion of their own biomass)"
INDIVIDUAL_BIOMASS = "Individual animal Biomass (kg)"
GROWTH_RATE_FACTOR = "Rate factor to grow towards limit by"
DECLINE_RATE_FACTOR = "Rate factor to decline towards limit by"

FOOD_WEB_GRAPH = {
    OSPREY: {
        REQUIRED_BIOMASS_FACTOR: 4,
        INDIVIDUAL_BIOMASS: 1,
        GROWTH_RATE_FACTOR: 1.115,
        DECLINE_RATE_FACTOR: 0.75,
        PREDATORS: [],
        PREY: [TROUT]
    },
    HERON: {
        REQUIRED_BIOMASS_FACTOR: 4,
        INDIVIDUAL_BIOMASS: 1.5,
        GROWTH_RATE_FACTOR: 1.115,
        DECLINE_RATE_FACTOR: 0.75,
        PREDATORS: [],
        PREY: [TROUT, FROG]
    },
    MOSQUITO: {
        REQUIRED_BIOMASS_FACTOR: 0,
        INDIVIDUAL_BIOMASS: 1e-3,
        GROWTH_RATE_FACTOR: 1.075,
        DECLINE_RATE_FACTOR: 0.9,
        PREDATORS: [FROG, TROUT],
        PREY: []
    },
    MAYFLY: {
        REQUIRED_BIOMASS_FACTOR: 1.5,
        INDIVIDUAL_BIOMASS: 1e-3,
        GROWTH_RATE_FACTOR: 1.075,
        DECLINE_RATE_FACTOR: 0.85,
        PREDATORS: [FROG, TROUT],
        PREY: [ALGAE]
    },
    FROG: {
        REQUIRED_BIOMASS_FACTOR: 1.5,
        INDIVIDUAL_BIOMASS: 15e-3,
        GROWTH_RATE_FACTOR: 1.1,
        DECLINE_RATE_FACTOR: 0.8,
        PREDATORS: [HERON, OTTER],
        PREY: [MOSQUITO, MAYFLY]
    },
    TROUT: {
        REQUIRED_BIOMASS_FACTOR: 1.5,
        INDIVIDUAL_BIOMASS: 3,
        GROWTH_RATE_FACTOR: 1.1,
        DECLINE_RATE_FACTOR: 0.8,
        PREDATORS: [HERON, OTTER, OSPREY],
        PREY: [MAYFLY, MOSQUITO]
    },
    OTTER: {
        REQUIRED_BIOMASS_FACTOR: 4,
        INDIVIDUAL_BIOMASS: 7,
        GROWTH_RATE_FACTOR: 1.115,
        DECLINE_RATE_FACTOR: 0.75,
        PREDATORS: [],
        PREY: [FROG, TROUT, MUSSELS]
    },
    ALGAE: {
        REQUIRED_BIOMASS_FACTOR: 0,
        INDIVIDUAL_BIOMASS: 1e-3,
        GROWTH_RATE_FACTOR: 1.01,
        DECLINE_RATE_FACTOR: 0.95,
        PREDATORS: [CATFISH, MAYFLY, MUSSELS],
        PREY: []
    },
    MUSSELS: {
        REQUIRED_BIOMASS_FACTOR: 1.5,
        INDIVIDUAL_BIOMASS: 0.05,
        GROWTH_RATE_FACTOR: 1.15,
        DECLINE_RATE_FACTOR: 0.85,
        PREDATORS: [OTTER],
        PREY: [ALGAE]
    },
    CATFISH: {
        REQUIRED_BIOMASS_FACTOR: 1.5,
        INDIVIDUAL_BIOMASS: 4,
        GROWTH_RATE_FACTOR: 1.1,
        DECLINE_RATE_FACTOR: 0.9,
        PREDATORS: [],
        PREY: [ALGAE]
    }
}

POPULATION = "The number of individuals in the population"
POP_CHANGE_FACTOR = "The factor by which the population will change this year"
POPULATION_BIOMASS = "Total biomass for entire species population"
BIOMASS_PER_PREDATOR = "The total amount of the population biomass available for consumption by each predator"
TOTAL_PREDATOR_BIOMASS = "The total amount of biomass across all the predators of this species"

PREDATION_PRESSURE = "A factor to represent how desperate each predator is.  <1 means easy life for prey.  >1 means sad times."

MIN_PREDATION_FACTOR = 1
MAX_PREDATION_FACTOR = 1.5


class PopSimCalculator:
    def __init__(self):
        self.__currentData = None

    def getSpeciesIDList(self):
        return list(FOOD_WEB_GRAPH.keys())

    def doSimulation(self, prevYearPopulations):
        self.__currentData = {}
        self.__populateCurrentData(prevYearPopulations)

        self.__calculatePopulationBiomassBySpecies()

        self.__calculateBiomassAvailableToPredators()

        self.__adjustGrowthForFoodAvailability()

        self.__adjustGrowthForPredatorPressure()

        newYearPopulations = self.__produceNewPopulationDict()

        self.__addMigratoryPressures(newYearPopulations)

        self.__currentData = None

        return newYearPopulations

    def __populateCurrentData(self, populations):
        for speciesID, population in populations.items():
            self.__currentData[speciesID] = {POPULATION: population,
                                             POP_CHANGE_FACTOR: 1,
                                             PREDATION_PRESSURE: {}}

    def __calculatePopulationBiomassBySpecies(self):
        for speciesID, data in self.__currentData.items():
            population = self.__currentData[speciesID][POPULATION]
            individualBiomass = FOOD_WEB_GRAPH[speciesID][INDIVIDUAL_BIOMASS]

            self.__currentData[speciesID][POPULATION_BIOMASS] = population*individualBiomass

    def __calculateBiomassAvailableToPredators(self):
        results = {}
        for speciesID, speciesData in self.__currentData.items():
            # calculate total biomass of predators
            grandTotalPredatorBiomass = 0.0
            for predatorSpeciesID in FOOD_WEB_GRAPH[speciesID][PREDATORS]:
                predatorSpeciesBiomass = self.__currentData[predatorSpeciesID][POPULATION_BIOMASS]
                grandTotalPredatorBiomass += predatorSpeciesBiomass
            speciesData[TOTAL_PREDATOR_BIOMASS] = grandTotalPredatorBiomass

            # divide this species' biomass between the predators, weighted by predator biomass
            biomassByPredator = {}
            if grandTotalPredatorBiomass > 0:
                thisSpeciesBiomass = self.__currentData[speciesID][POPULATION_BIOMASS]
                for predatorSpeciesID in FOOD_WEB_GRAPH[speciesID][PREDATORS]:
                    predatorSpeciesBiomass = self.__currentData[predatorSpeciesID][POPULATION_BIOMASS]

                    biomassByPredator[predatorSpeciesID] = (thisSpeciesBiomass * predatorSpeciesBiomass
                                                            / grandTotalPredatorBiomass)

            self.__currentData[speciesID][BIOMASS_PER_PREDATOR] = biomassByPredator

    def __adjustGrowthForFoodAvailability(self):
        for speciesID, speciesData in self.__currentData.items():
            if speciesData[POPULATION] > 0:
                # only apply food adjustment if species is actually a predator
                if len(FOOD_WEB_GRAPH[speciesID][PREY]) > 0:
                    totalAvailableBiomass = 0
                    for preySpeciesID in FOOD_WEB_GRAPH[speciesID][PREY]:
                        preyData = self.__currentData[preySpeciesID]
                        availablePreyBiomass = preyData[BIOMASS_PER_PREDATOR][speciesID]
                        totalAvailableBiomass += availablePreyBiomass

                    totalRequiredFoodBiomass = (speciesData[POPULATION_BIOMASS]
                                                * FOOD_WEB_GRAPH[speciesID][REQUIRED_BIOMASS_FACTOR])

                    # calculate and store pressure from this predator for each prey species
                    if totalAvailableBiomass > 0:
                        preyPredationPressure = totalRequiredFoodBiomass / totalAvailableBiomass
                        for preySpeciesID in FOOD_WEB_GRAPH[speciesID][PREY]:
                            preyData = self.__currentData[preySpeciesID]
                            preyData[PREDATION_PRESSURE][speciesID] = preyPredationPressure

                    # adjust the population growth rate for the predator
                    requiredBiomassForIndividual = (FOOD_WEB_GRAPH[speciesID][INDIVIDUAL_BIOMASS]
                                                    * FOOD_WEB_GRAPH[speciesID][REQUIRED_BIOMASS_FACTOR])
                    newPopulationLimit = int(totalAvailableBiomass / requiredBiomassForIndividual)
                    currentPopulation = speciesData[POPULATION]
                    if newPopulationLimit < currentPopulation:
                        speciesData[POP_CHANGE_FACTOR] *= FOOD_WEB_GRAPH[speciesID][DECLINE_RATE_FACTOR]
                    elif newPopulationLimit > currentPopulation:
                        speciesData[POP_CHANGE_FACTOR] *= FOOD_WEB_GRAPH[speciesID][GROWTH_RATE_FACTOR]
                else:
                    # allow normal growth rate if it does not require food
                    speciesData[POP_CHANGE_FACTOR] *= FOOD_WEB_GRAPH[speciesID][GROWTH_RATE_FACTOR]
    def __adjustGrowthForPredatorPressure(self):
        for speciesID, speciesData in self.__currentData.items():
            # only apply predator adjustment if species is actually prey
            if len(FOOD_WEB_GRAPH[speciesID][PREDATORS]) > 0:
                # if we sum all the predation factors weighted by the proportion of
                # predator biomass this should work out as a weighted average across
                # all predators
                totalPredatorBiomass = speciesData[TOTAL_PREDATOR_BIOMASS]
                totalPredationFactor = 0
                if totalPredatorBiomass > 0:
                    totalPredationFactor = 0
                    for predatorSpeciesID in FOOD_WEB_GRAPH[speciesID][PREDATORS]:
                        predatorData = self.__currentData[predatorSpeciesID]
                        # check there are any predators actually left to apply the pressure
                        if predatorSpeciesID in speciesData[PREDATION_PRESSURE]:
                            predationContribution = (speciesData[PREDATION_PRESSURE][predatorSpeciesID]
                                                     * predatorData[POPULATION_BIOMASS]
                                                     / totalPredatorBiomass)
                            totalPredationFactor += predationContribution

                if totalPredationFactor < MIN_PREDATION_FACTOR:
                    totalPredationFactor = MIN_PREDATION_FACTOR

                # stability fudge
                if totalPredationFactor > MAX_PREDATION_FACTOR:
                    totalPredationFactor = MAX_PREDATION_FACTOR

                speciesData[POP_CHANGE_FACTOR] /= totalPredationFactor

    def __produceNewPopulationDict(self):
        newPopulations = {}

        for speciesID, speciesData in self.__currentData.items():
            newPop = int(speciesData[POPULATION] * speciesData[POP_CHANGE_FACTOR])

            if newPop == speciesData[POPULATION]:
                if speciesData[POP_CHANGE_FACTOR] > 1:
                    newPop += 1
                elif speciesData[POP_CHANGE_FACTOR] < 1 and newPop > 0:
                    newPop -= 1

            newPopulations[speciesID] = newPop

        return newPopulations

    def __addMigratoryPressures(self, newPopulations):
        for speciesID in newPopulations.keys():
            popBiomass = self.__currentData[speciesID][POPULATION_BIOMASS]
            individualBiomass = FOOD_WEB_GRAPH[speciesID][INDIVIDUAL_BIOMASS]
            # if popBiomass < 5:
            #     newBiomass = uniform(1, 5)
            #     numNewIndividuals = int(newBiomass / individualBiomass)
            #     newPopulations[speciesID] += numNewIndividuals
            # elif individualBiomass > 0.1 and popBiomass > 1000:
            #     newBiomass = popBiomass * uniform(0.9, 0.95)
            #     numNewIndividuals = int(newBiomass / individualBiomass)
            #     newPopulations[speciesID] = numNewIndividuals
            # elif newPopulations[speciesID] > 2e6:
            #     newPopulations[speciesID] = int(newPopulations[speciesID] * uniform(0.85, 0.95))

            # if newPopulations[speciesID] == 0:
            #     newPopulations[speciesID] += int(uniform(0.5, 1.75))







