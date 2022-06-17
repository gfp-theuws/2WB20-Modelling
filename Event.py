class Event:

    GROUP_ARRIVAL = 0
    ELEVATOR_ARRIVAL = 1
    ELEVATOR_DEPARTURE = 2

    def __init__(self, typ, time, floor, task=None):
        self.type = typ
        self.time = time
        self.task = task
        self.floor = floor

    def __lt__(self, other):
        return self.time < other.time

    def __str__(self):
        s = ('Visitor arrival', 'Train arrival', 'Train departure')
        return s[self.type] + ' at t = '+str(self.time)

