import sys
import csv
import datetime
import copy
import random
import numpy as np

def make_dict(schedule, members, predict = None):
    if not predict is None:
        D = copy.deepcopy(predict)
    else:
        D = {}

        for m in members:
            D[m] = 0

    for i in schedule:
        if type(i) is str:
            D[i] += 1

    return D
    

# equality metric, lower is better
def equality(schedule, members, predict = None, itr = 1):
    D = make_dict(schedule, members, predict)
    
    best_avg = float(len(schedule)) / len(members) * itr
    ret = 0

    for i in D.values():
        ret += (i - best_avg) ** 2

    return ret

def schedule(days, slots_per_day, members, member_availability, predict = None, itr = 1):
    N = 300
    
    possible_solutions = [[False] * days * slots_per_day]

    for t in range(slots_per_day * days):
        eq = equality(possible_solutions[0], members, predict, itr)
        new_solutions = []
        choose = list(range(len(members)))
        while len(choose) > 0:
            R = random.randint(0, len(choose) - 1)
            m = choose[R]
            del choose[R]
            
            if member_availability[m][t]:
                for S in possible_solutions:
                    s = copy.deepcopy(S)
                    s[t] = members[m]
                    new_solutions.append(s)

        if len(new_solutions) > 0:
            next_sols = [new_solutions[0]]
            best = equality(new_solutions[0], members, predict, itr)
            for S in new_solutions[1:]:
                E = equality(S, members, predict, itr)
                if best > E:
                    best = E
                    next_sols = [S]
                elif best == E:
                    next_sols.append(S)
            if len(next_sols) > N:
                possible_solutions = random.sample(next_sols, N)
            else:
                possible_solutions = next_sols
                
    return possible_solutions

if __name__ == "__main__":
    filename = sys.argv[1]
    at_table = int(sys.argv[2])
    times = int(sys.argv[3])
    members = []
    times_available = []
    day_values = []
    start = None
    
    with open(filename) as f:
        reader = csv.reader(f, delimiter=',', quotechar='|')
        days = 0
        slots_per_day = 0
        for row in reader:
            try:
                T = datetime.datetime.strptime(row[0], "%H:%M")
                if start is None:
                    start = T
                    
                for i in range(1, len(row)):
                    times_available[-1][i - 1].append(row[i] == "TRUE")

                if len(times_available) == 1:
                    slots_per_day += 1
                    
            except ValueError:
                if len(times_available) > 0:
                    times_available[-1] = [item for sublist in times_available[-1] for item in sublist]

                if days == 0:
                    days = len(row) - 1
                    day_values = row[1:]
                    slots_per_day = 0
                    
                members.append(row[0])
                new_times = []
                for i in range(days):
                    new_times.append([])
                times_available.append(new_times)

        times_available[-1] = [item for sublist in times_available[-1] for item in sublist]

    # convert half hours to longer times...
    slots_per_day /= times
    hour_times = []
    for T in times_available:
        hour_times.append([])
        t = 0
        while t < len(T):
            b = True
            for i in range(times):
                if t + i < len(T) and not T[t + i]:
                    b = False
                    break
                
            hour_times[-1].append(b)
            
            t += times
            
    print "Making tabling schedule for the following members:"
    print members
    print ""
    S = []
    D = None
    for i in range(at_table):
        S.append(schedule(days, slots_per_day, members, hour_times, D, i + 1)[0])

        D = make_dict(S[-1], members, D)
        for t, m1 in enumerate(S[-1]):
            for idx, m in enumerate(members):
                if m1 == m:
                    hour_times[idx][t] = False

    with open('result.csv', 'w') as f:
        C = csv.writer(f)
        full_schedule = np.column_stack(S)
        C.writerow([''] + day_values)
        for t in range(slots_per_day):
            row = []
            curr_time = start + datetime.timedelta(minutes=30) * times * (t % slots_per_day)
            row.append(curr_time.strftime("%H:%M"))
            for d in range(days):
                string = ""
                for s in full_schedule[d * slots_per_day + t]:
                    string += s + " "
                row.append(string)
            print row
            C.writerow(row)
        
    print D
