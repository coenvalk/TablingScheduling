import AvailableTimes


class Member:
    def __init__(self, name, times_available):
        self.n_ = name
        self.times_ = times_available


    def Print(self):
        print(self.n_ + " available times:")
        self.times_.Print()

    def isAvailable(self, day, time):
        return self.times_.isAvailable(day, time)
