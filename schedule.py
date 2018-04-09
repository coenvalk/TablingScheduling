# Coen Valk, Spring 2018

"""
MIT License

Copyright (c) 2018 Coen Valk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


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

def schedule(Members, days, start, end, Bias, at_table):
    #print("scheduling members:")
    endindex = int(days * (end - start).seconds / 1800)
    S = []

    for i in range(len(Members)):
        # Members[i].Print()
        # print("")
        S.append([])
        for j in range(endindex):
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
        for j in range(1, endindex):
            previous_shift = True
            if j >= 4:
                for a in range(4):
                    if not S[i][j - a - 1] == Members[i].n_:
                        previous_shift = False
                        break
            else:
                previous_shift = False
            if not S[i][j]: # if already occupied, keep moving
                startj = j
                endj = j
                while endj < endindex and endj - startj <= 4:
                    I = index_to_daytime(endj, start, end)
                    D = I[0]
                    T = I[1]
                    if not Members[i].isAvailable(D, T):
                        break
                    else:
                        endj += 1
                endj -= 1
                if startj < endj:
                    I = index_to_daytime(endj, start, end)
                    D = I[0]
                    T = I[1]
                    assert Members[i].isAvailable(D, T)
                    B = endj - startj
                    empty = False
                    for a in range(endj - startj + 1): # make sure there are no empty shifts left!
                        if S[i - 1][j + a] == False:
                            empty = True
                            break
                    if not empty: # if it is not empty, check if it is better.
                        added = False
                        for B in range(endj - startj + 1, 2, -1):
                            # try to add all at once, then remove from end
                            for a in range(B):
                                S[i][j + a] = S[i - 1][j + a]
                            current = determine_fairness(S, Members, i, j + B - 1, Bias, at_table)
                            for a in range(B):
                                S[i][j + a] = Members[i].n_
                            now = determine_fairness(S, Members, i, j + B - 1, Bias, at_table)
                            if current >= now:
                                # print(S[i])
                                added = True
                                a = B
                                while j + a < endindex:
                                    S[i][j + a] = False
                                    a += 1
                                break
                        if not added:
                            I1 = index_to_daytime(startj, start, end)
                            D1 = I1[0]
                            T1 = I1[1]
                            I2 = index_to_daytime(endj, start, end)
                            D2 = I2[0]
                            T2 = I2[1]
                            for a in range(endj - startj + 1):
                                S[i][j + a] = S[i - 1][j + a]
                            while j + a < endindex:
                                S[i][j + a] = False
                                a += 1
                    else:
                        for a in range(endj - startj + 1):
                            S[i][j + a] = Members[i].n_
                        while j + a < endindex:
                            S[i][j + a] = False
                            a += 1
                else:
                    S[i][j] = S[i - 1][j]
                                
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
    
    for i in range(endindex):
        I = index_to_daytime(i, start, end)
        D = I[0]
        T = I[1]
        #print(T.strftime("%H:%M"), end="\t")
        # print(S[-1][int((T - start).seconds / 1800) + i * int((end - start).seconds / 1800)], end="\t")
        for M in Members:
            if S[-1][i] == M.n_:
                M.SetUnavailable(D, T)
        #print("")
    return S[-1]

def full_schedule(Members, days, start, end, at_table, outFile):
    Bias = {}
    S = []
    for i in range(at_table):
        S.append(schedule(Members, days, start, end, Bias, at_table))

    outFile.write(",")
    print("\t", end="")
    for i in range(days):
        print("Day " + str(i + 1), end="")
        outFile.write("Day " + str(i + 1) + ",")
        for j in range(at_table):
            print("\t", end="")
    outFile.write('\n')
    print("")
    
    T = start
    while int((end - T).seconds / 1800) > 0:
        print(T.strftime("%H:%M"), end="\t")
        outFile.write(T.strftime("%H:%M") + ",")
        for i in range(days):
            for j in range(at_table):
                index = int((T - start).seconds / 1800) + i * int((end - start).seconds / 1800)
                print(S[j][index], end=" ")
                outFile.write(str(S[j][index]) + " ")
            outFile.write(",")
            print("\t", end="")
        outFile.write('\n')
        print("")
        T += datetime.timedelta(minutes=30)

    sum = 0
    for key in sorted(Bias.keys()):
        print(key + ": " + str(Bias[key] / 2) + "hrs.")
        sum += Bias[key] / 2
    print("Total: " + str(sum))

    
def main():
    START = datetime.datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    END = datetime.datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)

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

                
                available = AvailableTimes(START, END, len(row) - 1)
                days = len(row) - 1

    with open('outFile.csv', 'w', newline='') as outFile:
        M = Member(name, available)
        Members.append(M)
        full_schedule(Members, days, START, END, 2, outFile)

main()
