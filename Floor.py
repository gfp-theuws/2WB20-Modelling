from collections import deque
import numpy as np

class Floor:

    def __init__(self, nr):
        self.id = nr
        self.queueLength = 0
        self.hasElevator = np.array([])