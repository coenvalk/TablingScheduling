# Coen Valk, Spring 2018

import datetime
from AvailableTimes import AvailableTimes
from Member import Member

# returns the sum of the deviation from the average for all members
# NOTE: only determines based on values M (members) and T (current time index)
def determine_fairness(S, Members, M, T):
    avg = (T + 1) / (M + 1)
    D = {}
    for i in range(M + 1):
        D[Members[i].n_] = 0
        
    for i in range(T + 1):
        if not S[M][i] == False:
            D[S[M][i]] += 1

    sum = 0
    for key, value in D.items():
        sum += abs(avg - value)
    return sum

# returns a tuple, with index 0 being the day, index 1 being the time
def index_to_daytime(index, start, end):
    day = int(index / ((end - start).seconds / 1800))
    if index % 2 == 0:
        time = start + datetime.timedelta(hours = int((index % ((end - start).seconds / 1800)) / 2))
    else:
        time = start + datetime.timedelta(hours = int((index % ((end - start).seconds / 1800)) / 2), minutes=30)
        
    return(day, time)

def schedule(Members, days, start, end):
    print("scheduling members:")
    S = []
    for i in range(len(Members)):
        # Members[i].Print()
        # print("")
        S.append([])
        for j in range(int(days * (end - start).seconds / 1800)):
            S[i].append(False) # will be possible list and times of people to schedule
            
                
    for j in range(len(S[0])):
        # initial member does every shift they can
        I = index_to_daytime(j, start, end)
        D = I[0]
        T = I[1]
        if Members[0].isAvailable(D, T):
            S[0][j] = Members[0].n_
        else:
            S[0][j] = False

    for i in range(1, len(S)):
        I = index_to_daytime(0, start, end)
        D = I[0]
        T = I[1]
        if Members[i].isAvailable(D, T):
            S[i][0] = Members[i].n_
        else:
            S[i][0] = S[i-1][0]
    # We want to increase by time fast, and by people slowly:
    for i in range(1, len(Members)):
        for j in range(1, days * int((end - start).seconds / 1800)):
            I = index_to_daytime(j, start, end)
            D = I[0]
            T = I[1]
            if Members[i].isAvailable(D, T):
                if S[i - 1][j] == False:
                    S[i][j] = Members[i].n_
                else:
                    S[i][j] = S[i - 1][j]
                    current = determine_fairness(S, Members, i, j)
                    S[i][j] = Members[i].n_
                    now = determine_fairness(S, Members, i, j)
                    if current < now:
                        S[i][j] = S[i - 1][j]
            else:
                S[i][j] = S[i - 1][j]

    # if I did my homework, this should be at least close to the correct solution!
    # print(S[-1])

    # now we print it out nice and pretty:
    print("\t", end="")
    for i in range(days):
        print("Day " + str(i + 1), end="\t")
    print("")
    
    T = start
    while int((end - T).seconds / 1800) > 0:
        print(T.strftime("%H:%M"), end="\t")
        for i in range(days):
            print(S[-1][int((T - start).seconds / 1800) + i * int((end - start).seconds / 1800)], end="\t")
        print("")
        T += datetime.timedelta(minutes=30)

    
def main():
    START = datetime.datetime.now().replace(hour=9, minute=0)
    END = datetime.datetime.now().replace(hour=12, minute=0)
    
    a = AvailableTimes(START, END, 3)
    b = AvailableTimes(START, END, 3)
    c = AvailableTimes(START, END, 3)

    T1 = datetime.datetime.now().replace(hour=9, minute=0)
    T2 = datetime.datetime.now().replace(hour=10, minute=0)
    
    a.SetAvailableRange(0, T1, T2)

    T1 = datetime.datetime.now().replace(hour=11, minute=0)
    T2 = datetime.datetime.now().replace(hour=11, minute=30)

    a.SetAvailableRange(0, T1, T2)

    T1 = datetime.datetime.now().replace(hour=9, minute=0)
    a.SetAvailable(1, T1)
    
    T1 = datetime.datetime.now().replace(hour=10, minute=0)
    a.SetAvailable(1, T1)
    
    T1 = datetime.datetime.now().replace(hour=11, minute=0)
    a.SetAvailable(1, T1)

    T1 = datetime.datetime.now().replace(hour=9, minute=0)
    T2 = datetime.datetime.now().replace(hour=10, minute=0)
    a.SetAvailableRange(2, T1, T2)

    T1 = datetime.datetime.now().replace(hour=11, minute=0)
    T2 = datetime.datetime.now().replace(hour=11, minute=30)
    a.SetAvailableRange(2, T1, T2)

    Coen = Member("Corn", a)

    T1 = datetime.datetime.now().replace(hour=9, minute=30)
    b.SetAvailable(0, T1)

    T1 = datetime.datetime.now().replace(hour=10, minute=30)
    T2 = datetime.datetime.now().replace(hour=11, minute=0)

    b.SetAvailableRange(0, T1, T2)

    T1 = datetime.datetime.now().replace(hour=9, minute=30)
    b.SetAvailable(1, T1)
    
    T1 = datetime.datetime.now().replace(hour=10, minute=30)
    b.SetAvailable(1, T1)
    
    T1 = datetime.datetime.now().replace(hour=11, minute=30)
    b.SetAvailable(1, T1)

    T1 = datetime.datetime.now().replace(hour=10, minute=0)
    T2 = datetime.datetime.now().replace(hour=11, minute=0)
    b.SetAvailableRange(2, T1, T2)
    
    Sage = Member("Sage", b)

    T1 = datetime.datetime.now().replace(hour=9, minute=30)
    T2 = datetime.datetime.now().replace(hour=10, minute=0)

    c.SetAvailableRange(0, T1, T2)

    T1 = datetime.datetime.now().replace(hour=9, minute=0)
    c.SetAvailable(1, T1)
    
    T1 = datetime.datetime.now().replace(hour=10, minute=0)
    c.SetAvailable(1, T1)
    
    T1 = datetime.datetime.now().replace(hour=11, minute=0)
    c.SetAvailable(1, T1)

    T1 = datetime.datetime.now().replace(hour=10, minute=30)
    T2 = datetime.datetime.now().replace(hour=11, minute=30)
    c.SetAvailableRange(2, T1, T2)
    
    Jordan = Member("Jordan", c)
    
    Members = [Coen, Sage, Jordan]

    schedule(Members, 3, START, END)


main()
