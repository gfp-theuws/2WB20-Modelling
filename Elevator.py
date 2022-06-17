from collections import deque

class Elevator:

    def __init__(self, nr):
        self.id = nr
        self.passengers = deque()
        self.floor = 0
        self.movingDown = False