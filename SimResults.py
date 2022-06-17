import numpy as np

class SimResults:

    MAX_QL = 10000

    def __init__(self):
        self.sumW = 0
        self.sumW2 = 0
        self.tOld = 0
        self.sumsQL = [0, 0, 0, 0]
        self.sumsQL2 = [0, 0, 0, 0]
        self.nrCust = 0
        self.passengersLeft = [0, 0, 0, 0]
        self.QLHist = [np.zeros(self.MAX_QL + 1), np.zeros(self.MAX_QL + 1), np.zeros(self.MAX_QL + 1), np.zeros(self.MAX_QL + 1)]
        self.dailyCost = 0

    def registerWaitingTime(self, t, vis):
        st = t - vis.arrivalTime
        self.sumW += st
        self.sumW2 += st**2
        self.nrCust += 1

    def getMeanWaitingTime(self):
        return self.sumW / self.nrCust

    def getWaitingTimesVariance(self):
        m2 = self.sumW2 / self.nrCust
        m1 = self.getMeanWaitingTime()
        return m2 - m1 * m1

    # def registerQueueLengths(self, t, queues):
    #     q = [0, 0, 0, 0]
    #     for i in range(4):
    #         for j in range(len(queues[i])):
    #             q[i] += queues[i][j].size
    #     dt = t - self.tOld
    #     self.tOld = t
    #     for i in range(0, 4):
    #         self.QLHist[i][q[i]] += dt
    #         self.sumsQL[i] += q[i] * dt
    #         self.sumsQL2[i] += q[i] * q[i] * dt
    #
    # def getMeanQueueLength(self, QL):
    #     return QL / self.tOld
    #
    # def getQueueLengthVariance(self, QL, QL2):
    #     m2 = QL2 / self.tOld
    #     m1 = self.getMeanQueueLength(QL)
    #     return m2 - m1 * m1

    # def getElevatorIdleTimeFraction(self):
    #     return self.sumI / self.tOld
    #
    # def getQueueLengthHistogram(self):
    #     return self.qlHist / self.tOld
    

    def __str__(self):
        s = ''
        # for i in range(0, 4):
        #     s += 'Mean queue length at station ' + str(i + 1) + ': ' + str(self.getMeanQueueLength(self.sumsQL[i])) + '\n'
        #     s += 'variance queue length at station 1: ' + str(self.getQueueLengthVariance(self.sumsQL[i], self.sumsQL2[i])) + '\n\n'
        s += 'Mean waiting time: ' + str(round(self.getMeanWaitingTime(), 3)) + ' +- ' + str(round(1.96*self.getWaitingTimesVariance()/(np.sqrt(self.nrCust)), 3)) + '\n'
        s += 'Variance waiting time: ' + str(round(self.getWaitingTimesVariance(), 3)) + '\n\n'
        # s += 'Probability of the train leaving a stop with no people waiting to board: ' + str(self.getPassengersLeftProb()[0]) + '\n'
        # s += 'Probability of the train leaving a stop with 1 to 24 people still waiting to board: ' + str(self.getPassengersLeftProb()[1]) + '\n'
        # s += 'Probability of the train leaving a stop with 25 to 49 people still waiting to board: ' + str(self.getPassengersLeftProb()[2]) + '\n'
        # s += 'Probability of the train leaving a stop with 50 or more people still waiting to board: ' + str(self.getPassengersLeftProb()[3]) + '\n'
        # s += 'Fraction idle time: ' + str(self.getServerIdleTimeFraction()) + '\n'
        # hist = self.getQueueLengthHistogram()
        # for i in range(11):
        #     s += 'P(Q = '+str(i)+') = '+str(hist[i])+'\n'
        return s
