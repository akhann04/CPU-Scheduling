#SOURCES USED GPT, GITHUB COPILOT 


from dataclasses import dataclass
from collections import deque


# Class to store information about each process
@dataclass
class Process:
    pid: str
    arrival: int
    cpu_burst: int


# SJF Scheduler (Non-Preemptive)
# Returns timeline, completion times, TAT, and ATT
def sjf(processes):

    # Sort processes by arrival time
    not_arrived = sorted(processes, key=lambda p: (p.arrival, p.pid))

    # List of processes that have arrived
    ready = []

    # Remaining CPU burst time for each process
    remaining = {p.pid: p.cpu_burst for p in processes}

    # Store scheduling timeline
    timeline = []

    # Store completion times
    completion = {}

    # Start time
    t = 0

    # Keep running until all processes finish
    while not_arrived or ready:

        # Add processes that have arrived
        while not_arrived and not_arrived[0].arrival <= t:
            ready.append(not_arrived.pop(0))

        # If no process is ready, move to next arrival
        if not ready:
            t = not_arrived[0].arrival
            continue

        # Choose process with shortest CPU burst
        # Break ties using arrival time, then process ID
        ready.sort(key=lambda p: (p.cpu_burst, p.arrival, p.pid))

        current = ready.pop(0)

        # Record start and finish times
        start = t
        end = t + remaining[current.pid]

        timeline.append((current.pid, start, end))

        # Update completion time
        completion[current.pid] = end

        # Move time forward
        t = end

        remaining[current.pid] = 0

    # Calculate turnaround time
    tat = {}

    for p in processes:
        tat[p.pid] = completion[p.pid] - p.arrival

    # Calculate average turnaround time
    att = sum(tat.values()) / len(processes)

    return timeline, completion, tat, att


# SRT Scheduler (Preemptive Shortest Remaining Time)
def srt(processes):
    not_arrived = sorted(processes, key=lambda p: (p.arrival, p.pid))
    remaining = {p.pid: p.cpu_burst for p in processes}
    timeline = []
    completion = {}
    ready = []
    t = 0

    # run until all processes complete
    while any(remaining[pid] > 0 for pid in remaining):
        # add arrivals
        while not_arrived and not_arrived[0].arrival <= t:
            ready.append(not_arrived.pop(0))

        # pick candidates with remaining > 0
        candidates = [p for p in ready if remaining[p.pid] > 0]

        if not candidates:
            if not_arrived:
                t = not_arrived[0].arrival
                continue
            else:
                break

        # choose shortest remaining (tie by arrival then pid)
        candidates.sort(key=lambda p: (remaining[p.pid], p.arrival, p.pid))
        chosen = candidates[0]

        # run for 1 time unit
        start = t
        end = t + 1

        # merge with previous segment if same pid and contiguous
        if timeline and timeline[-1][0] == chosen.pid and timeline[-1][2] == start:
            pid, s, _ = timeline[-1]
            timeline[-1] = (pid, s, end)
        else:
            timeline.append((chosen.pid, start, end))

        remaining[chosen.pid] -= 1
        t = end

        if remaining[chosen.pid] == 0:
            completion[chosen.pid] = t
            # remove from ready
            if chosen in ready:
                ready.remove(chosen)

    # ensure completion times exist for all
    for p in processes:
        if p.pid not in completion:
            completion[p.pid] = t

    tat = {p.pid: completion[p.pid] - p.arrival for p in processes}
    att = sum(tat.values()) / len(processes)
    return timeline, completion, tat, att


# Test processes
processes = [
    Process("p1", 0, 3),
    Process("p2", 2, 6),
    Process("p3", 4, 4),
    Process("p4", 6, 5),
    Process("p5", 8, 2)
]


# Run SJF
timeline, completion, tat, att = sjf(processes)


# Display results
print("SJF Scheduling Timeline:")
for pid, start, end in timeline:
    print(f"{pid}: [{start}-{end}]")

print("\nTurnaround Times:")
for pid in sorted(tat):
    print(f"{pid}: {tat[pid]}")

print("\nAverage Turnaround Time:", att)




#ROUND ROBIN 

def round_robin (processes,quantum=2): 
    
    #SORTING PROCESSES BY THEIR ARRIVAL TIME 
    not_arrived = sorted (processes,key=lambda p: (p.arrival, p.pid))

    ready = deque() #FIFO READY QUEUE

    remaining = {p.pid: p.cpu_burst for p in processes} #REMAINING CPU BURST FOR EACH PROCESSES 

   #STORING SCHEDUELING TIME  
    timeline =[]

    #STORING COMPLETION TIME 
    completion ={}

    t = 0 #STARTING TIME 

    # KEEP RUNNING UNTIL ALL THE PROCESSES FINISH
    while not_arrived or ready:
        while not_arrived and not_arrived[0].arrival <= t:  # ADD PROCESSES THAT HAVE ARRIVED
            ready.append(not_arrived.pop(0))

        # IF NO PROCESS IS READY MOVE TIME TO THE NEXT ARRIVAL
        if not ready:
            t = not_arrived[0].arrival
            continue

        # CHOOSING THE FIRST PROCESS IN THE QUEUE
        current = ready.popleft()

        #RUNNING FOR 2 MS OR <
        run_time = min(quantum, remaining[current.pid])

        start = t 
        end = t + run_time

        #RECODRING START AND FINISH TIME
        timeline.append((current.pid, start, end))
           
        #UPDATE CURRENT TIME
        t = end
        remaining[current.pid] -= run_time



        # ADD NEWLY ARRIVED PROCESSES TO THE QUEUE
        while not_arrived and not_arrived[0].arrival <= t:
            ready.append(not_arrived.pop(0))

        # IF PROCESS IS NOT COMPLETED, PUT IT BACK IN THE QUEUE
        if remaining[current.pid] > 0:
            ready.append(current)
        else:
            # PROCESS IS COMPLETED
            completion[current.pid] = t

    # Calculate turnaround times for Round Robin
    tat = {}

    for p in processes:
        tat[p.pid] = completion[p.pid] - p.arrival

    # Calculate average turnaround time
    att = sum(tat.values()) / len(processes)

    return timeline, completion, tat, att


# ROUND ROBIN TEST CASES
rr_processes = [
    Process("p1", 0, 2),
    Process("p2", 1, 1),
    Process("p3", 2, 8),
    Process("p4", 3, 4),
    Process("p5", 4, 5)
]

# RUN ROUND ROBIN
rr_timeline, rr_completion, rr_tat, rr_att = round_robin(rr_processes, quantum=2)

# DISPLAY ROUND ROBIN RESULTS
print("\nRound Robin Scheduling Timeline:")
for pid, start, end in rr_timeline:
    print(f"{pid}: [{start}-{end}]")

print("\nRound Robin Turnaround Times:")
for pid in sorted(rr_tat):
    print(f"{pid}: {rr_tat[pid]}")

print("\nRound Robin Average Turnaround Time:", rr_att)



# Run SRT using the srt implementation above
srt_timeline, srt_completion, srt_tat, srt_att = srt(processes)

print("\nSRT Scheduling Timeline:")
for pid, start, end in srt_timeline:
    print(f"{pid}: [{start}-{end}]")

print("\nSRT Turnaround Times:")
for pid in sorted(srt_tat):
    print(f"{pid}: {srt_tat[pid]}")

print("\nSRT Average Turnaround Time:", srt_att)
