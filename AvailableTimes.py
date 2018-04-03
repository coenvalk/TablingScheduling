import datetime

class AvailableTimes:
    # Initializes everything to be UNAVAILABLE
    # tim intervals are by half hours between end_time and start_time
    def __init__(self, start_time, end_time, days):
        self.start_ = start_time
        self.end_ = end_time
        self.days_ = days
        self.times_ = []
        for i in range(days):
            self.times_.append([])
            for j in range(int((end_time - start_time).seconds / 1800)):
                self.times_[i].append(False) # false in UNavailable, true is available

    def isAvailable(self, day, time):
        return self.times_[day][int((time - self.start_).seconds / 1800)]
                
    # sets the time at certain value available
    def SetAvailable(self, day, time):
        self.times_[day][int((time - self.start_).seconds / 1800)] = True

    def SetAvailableRange(self, day, start, end):
        T = start
        while T <= end:
            self.SetAvailable(day, T)
            T += datetime.timedelta(minutes=30)
        
    # prints out the available times
    def Print(self):
        print("\t", end="")
        for i in range(self.days_):
            print("Day " + str(i + 1), end="\t")
        print("")

        T = self.start_
        while int((self.end_ - T).seconds / 1800) > 0:
            print(T.strftime("%H:%M"), end="\t")
            for i in range(self.days_):
                print(self.times_[i][int((T - self.start_).seconds / 1800)], end="\t")
            print("")
            T += datetime.timedelta(minutes=30)
