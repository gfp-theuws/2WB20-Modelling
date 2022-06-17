#Importing the needed libraries

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
from FES import FES
from Event import Event
from SimResults import SimResults
from Elevator import Elevator
from Floor import Floor
from Visitor import Visitor
from collections import deque
import time
import random

class Metaforum:

    def __init__(self, maxPeople, arrivalFreq, nrElevators, nrFloors, elevatorCapacity, verbose=False):
        self.maxPeople = maxPeople
        self.arrivalProb = arrivalFreq  # The frequency of arrivals
        self.nrElevators = nrElevators  # The number of elevators in the system.
        self.nrFloors = nrFloors  # The number of floors in the building
        self.elevatorCapacity = elevatorCapacity
        self.verbose = verbose  # If True, detailed data about the simulation will be printed.

    def simulate(self):
        results = SimResults()
        t = 0
        # Simulation time steps
        simTime = 100000
        # Counter for visitors.
        nrVisitors = 0

        elevators = [None for _ in range(nrElevators)]

        floors = [None] * self.nrFloors
        queues = np.zeros(self.nrFloors, dtype=object)
        for i in range(len(queues)):
            queues[i] = deque()

        travelProb = np.zeros((self.nrFloors, self.nrFloors))
        for i in range(self.nrFloors):
            for j in range(self.nrFloors):
                if i != j:
                    travelProb[i][j] = 1 / (self.nrFloors - 1)

        for i in range(self.nrFloors):
            floors[i] = Floor(i)

        for i in range(self.nrElevators):
            elevators[i] = Elevator(i)

        while t < simTime:
            t += 1

            nrInSystem = 0
            newPass = 0
            for i in range(self.nrFloors):
                nrInSystem += len(queues[i])
            for i in range(self.nrElevators):
                nrInSystem += len(elevators[i].passengers)

            for i in range(self.nrFloors):
                x = np.random.uniform(0, 1)
                if x < self.arrivalProb and nrInSystem < maxPeople:
                    nrVisitors += 1
                    newPass += 1
                    nrInSystem += 1

            for i in range(newPass):
                f = random.choice(list(range(nrFloors)))
                destination = random.choices(list(range(self.nrFloors)), weights=travelProb[i])[0]
                vis = Visitor(nrVisitors, t, destination)
                goToQueue = True
                availElev = []
                for j in range(self.nrElevators):
                    if len(elevators[j].passengers) < self.elevatorCapacity and elevators[j].floor == f:
                        goToQueue = False
                        availElev.append(j)
                if goToQueue:
                    queues[f].append(vis)
                else:
                    elevators[random.choice(availElev)].passengers.append(vis)
                    results.registerWaitingTime(t, vis)

            for i in range(self.nrElevators):
                currFloor = elevators[i].floor
                moveDown = elevators[i].movingDown
                elevStay = False
                if moveDown == False:
                    moveDown = True
                    for j in range(len(elevators[i].passengers)):
                        if (elevators[i].passengers[j].destination > currFloor) == moveDown:
                            moveDown = False
                    for n in range(int(currFloor), self.nrFloors):
                        if len(queues[n]) > 0:
                            moveDown = False
                elif moveDown == True:
                    moveDown = False
                    for j in range(len(elevators[i].passengers)):
                        if (elevators[i].passengers[j].destination < currFloor) != moveDown:
                            moveDown = True
                    for n in range(0, int(currFloor)):
                        if len(queues[n]) > 0:
                            moveDown = True
                if len(elevators[i].passengers) == 0:
                    elevStay = True
                    for m in range(self.nrFloors):
                        if len(queues[m]) > 0:
                            elevStay = False

                if currFloor == 0:
                    moveDown = False
                elif currFloor == nrFloors - 1:
                    moveDown = True

                if moveDown:
                    elevators[i].movingDown = True
                else:
                    elevators[i].movingDown = False

                elevators[i].floor = currFloor + 2*(int(not(moveDown)) - 0.5) * 0**elevStay
            for i in range(self.nrElevators):
                leavingPass = []
                f = int(elevators[i].floor)
                for j in range(len(elevators[i].passengers)):
                    if elevators[i].passengers[j].destination == f:
                        leavingPass.append(j)
                for k in reversed(leavingPass):
                    del elevators[i].passengers[k]
                boardingPass = []
                for n in range(len(queues[f])):
                    if self.elevatorCapacity > len(elevators[i].passengers):
                        boardingPass.append(n)
                        results.registerWaitingTime(t, queues[f][n])
                        elevators[i].passengers.append(queues[f][n])
                for k in reversed(boardingPass):
                    del queues[f][k]
        return results

# Defines the elevator + floor configuration
nrElevators = 1
nrFloors = 3
elevatorCapacity = 1
maxPeople = 1

arrivalProb = 0.3

# The simulation
sim = Metaforum(maxPeople, arrivalProb, nrElevators, nrFloors, elevatorCapacity)
res = sim.simulate()
print(res)
