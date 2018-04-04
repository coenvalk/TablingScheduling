# Coen Valk, Spring 2018

import datetime
import time
from AvailableTimes import AvailableTimes
from Member import Member
import csv

# returns the sum of the deviation from the average for all members
# NOTE: only determines based on values M (members) and T (current time index)
def determine_fairness(S, Members, M, T, Bias, at_table):
    avg = len(S[M]) / len(S) * at_table
    D = Bias.copy()
    for i in range(len(Members)):
        if not Members[i].n_ in D.keys():
            D[Members[i].n_] = 0
        
    for i in range(T + 1):
        if not S[M][i] == False:
            D[S[M][i]] += 1

    print(D)
    sum = 0
    for key, value in D.items():
        sum += abs(avg - value)
    print(sum)
    return sum

# returns a tuple, with index 0 being the day, index 1 being the time
def index_to_daytime(index, start, end):
    day = int(index / ((end - start).seconds / 1800))
    if index % 2 == 0:
        time = start + datetime.timedelta(hours = int((index % ((end - start).seconds / 1800)) / 2))
    else:
        time = start + datetime.timedelta(hours = int((index % ((end - start).seconds / 1800)) / 2), minutes=30)
        
    return(day, time)

def schedule(Members, days, start, end, Bias, at_table):
    #print("scheduling members:")
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

    B = 2
    # We want to increase by time fast, and by people slowly:
    for i in range(1, len(Members)):
        for j in range(1, days * int((end - start).seconds / 1800) - B):
            empty = True
            for a in range(B):
                if S[i][j + a]:
                    empty = False
                    break
            if empty:
                available = True
                for a in range(B):
                    I = index_to_daytime(j + a, start, end)
                    D = I[0]
                    T = I[1]
                    if not Members[i].isAvailable(D, T):
                        available = False
                        break
                if available:
                    empty = False
                    for a in range(B):
                        if not S[i - 1][j + a]:
                            empty = True
                            break
                    if empty:
                        # make this a thing:
                        for a in range(B):
                            S[i][j + a] = Members[i].n_
                    else:
                        # compare to current solution:
                        for a in range(B):
                            S[i][j + a] = S[i - 1][j + a]
                        current = determine_fairness(S, Members, i, j + B, Bias, at_table)
                        for a in range(B):
                            S[i][j + a] = Members[i].n_
                        now = determine_fairness(S, Members, i, j + B, Bias, at_table)
                        if current <= now:
                            # last solution was better....
                            for a in range(B):
                                S[i][j + a] = S[i - 1][j + a]
                else:
                    for a in range(B):
                        S[i][j + a] = S[i - 1][j + a]
                    
                                
    # if I did my homework, this should be at least close to the correct solution!
    # print(S[-1])

    # now we print it out nice and pretty:
    #print("\t", end="")
    #for i in range(days):
        #print("Day " + str(i + 1), end="\t")
    #print("")

    for M in S[-1]:
        if not M == False:
            if M in Bias.keys():
                Bias[M] += 1
            else:
                Bias[M] =  1
    
    T = start
    while int((end - T).seconds / 1800) > 0:
        #print(T.strftime("%H:%M"), end="\t")
        for i in range(days):
            # print(S[-1][int((T - start).seconds / 1800) + i * int((end - start).seconds / 1800)], end="\t")
            for M in Members:
                if S[-1][int((T - start).seconds / 1800) + i * int((end - start).seconds / 1800)] == M.n_:
                    M.SetUnavailable(i, T)
        #print("")
        T += datetime.timedelta(minutes=30)
    return S[-1]

def full_schedule(Members, days, start, end, at_table):
    Bias = {}
    S = []
    for i in range(at_table):
        S.append(schedule(Members, days, start, end, Bias, at_table))

    print("\t", end="")
    for i in range(days):
        print("Day " + str(i + 1), end="")
        for j in range(at_table):
            print("\t", end="")
    print("")
    
    T = start
    while int((end - T).seconds / 1800) > 0:
        print(T.strftime("%H:%M"), end="\t")
        for i in range(days):
            for j in range(at_table):
                print(S[j][int((T - start).seconds / 1800) + i * int((end - start).seconds / 1800)], end=" ")
            print("\t", end="")
        print("")
        T += datetime.timedelta(minutes=30)

    sum = 0
    for key in sorted(Bias.keys()):
        print(key + ": " + str(Bias[key] / 2) + "hrs.")
        sum += Bias[key] / 2
    print("Total: " + str(sum))

    
def main():
    START = datetime.datetime.now().replace(hour=9, minute=0)
    END = datetime.datetime.now().replace(hour=17, minute=0)

    Members = []
    available = False # first occurance

    with open('times.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            # first element of row must be a time... if not, we have a new person on our hands!
            try:
                T = datetime.datetime.strptime(row[0], "%I:%M:%S %p")
                for i in range(1, len(row)):
                    if row[i] == "TRUE":
                        available.SetAvailable(i - 1, T)
            except ValueError: # found a new person!
                if available: # not the first person we've seen
                    M = Member(name, available) # create member and availability times
                    Members.append(M)
                    
                name = row[0]
                # TODO: make this possible to accept different times, but good for now I guess
                START = datetime.datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
                END = datetime.datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)

                
                available = AvailableTimes(START, END, len(row) - 1)
                days = len(row) - 1

    M = Member(name, available)
    Members.append(M)
    full_schedule(Members, days, START, END, 2)

main()
