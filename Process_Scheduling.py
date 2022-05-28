#                                                <- Jay Shree Krishna ->
#                                                <-  Jay Swaminarayan ->
from tkinter import *
import os
import sys
import matplotlib.pyplot as plt
import random

def Plot(time_schedule):
    y_axis = []
    for process in time_schedule:
        list_of_pairs = []
        for i in range(len(process.marks)):
            if i % 2 == 0:
                pair = (process.marks[i], process.marks[i + 1] - process.marks[i])
                list_of_pairs.append(pair)
        y_axis.append(list_of_pairs)

    plt.ylim(0, len(time_schedule) * 10)
    # Setting X-axis limits
    max_X = 0
    for process in time_schedule:
        if process.marks[-1] > max_X:
            max_X = process.marks[-1]

    plt.xlim(0, max_X)

    plt.xlabel('time (ms)')
    plt.ylabel('Processes')

    tick_names = []
    tick_places = []
    for i in range(len(time_schedule)):
        tick_places.append(i * 10)
        tick_names.append(str(time_schedule[i].ID))
    plt.yticks(tick_places, tick_names)
    plt.grid(True)
    for i in range(len(time_schedule)):
        # print(y_axis[i])
        plt.broken_barh(y_axis[i], (i * 10, 10), facecolors=(random.random(), random.random(), random.random()))

    plt.plot()
    plt.show()

class process(object):
    def __init__(self, arrival_time, Duration, ID):
        self.ID = ID
        self.time_remaining = Duration
        self.duration = Duration
        self.arrival_time = arrival_time
        self.marks = []

    def pass_time(self):
        self.time_remaining = round(self.time_remaining - 0.1, 1)

    def addMark(self, time):
        self.marks.append(time)

class TimeQueue(object):
    def __init__(self):
        self.queue = []

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def put(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    def get(self):
        try:
            min = 0
            for i in range(len(self.queue)):
                if self.queue[i].time_remaining < self.queue[min].time_remaining:
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except IndexError:
            print('Index out of range.')
            exit()

class SimpleQueue(object):
    def __init__(self):
        self.queue = []

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def put(self, data):
        self.queue.append(data)

    # for popping an element
    def get(self):
        if self.isEmpty():
            print('Queue is empty')
        else:
            item = self.queue[0]
            del self.queue[0]
            return item

def FCFS(time_schedule):
    time = time_schedule[0].arrival_time
    for process in time_schedule:
        process.addMark(time)
        time = time + process.duration
        process.addMark(time)

def SJF(time_schedule):
    for e in range(len(time_schedule)):
        if time_schedule[0].arrival_time == time_schedule[e].arrival_time:
            if time_schedule[0].duration > time_schedule[e].duration:
                temp = time_schedule[e]
                # print(temp.duration)
                time_schedule[e] = time_schedule[0]
                time_schedule[0] = temp
        # print(time_schedule[e].duration)
    time = time_schedule[0].arrival_time

    for i in range(len(time_schedule)):
        time_schedule[i].addMark(time)
        time = time + time_schedule[i].duration
        time_schedule[i].addMark(time)
        if i < len(time_schedule) - 1:
            min = time_schedule[i + 1].duration
            c = i + 1
            for j in range(c, len(time_schedule)):
                if time > time_schedule[j].arrival_time:
                    if min > time_schedule[j].duration:
                        min = time_schedule[j].duration
                        temp = time_schedule[c]
                        time_schedule[c] = time_schedule[j]
                        time_schedule[j] = temp

def SRTF(time_schedule):
    all_at_sametime = True
    for process in time_schedule:
        if process.arrival_time != time_schedule[0].arrival_time:
            all_at_sametime = False
            break
    if all_at_sametime:
        time_schedule.sort(key=lambda x: x.time_remaining)
    time = 0
    index = 0
    current_procces = None
    queue = TimeQueue()
    while True:
        if index < len(time_schedule):
            if time >= time_schedule[index].arrival_time:
                new_process = time_schedule[index]
                if current_procces == None:
                    current_procces = new_process
                    current_procces.addMark(time)
                else:
                    queue.put(new_process)
                    current_procces.addMark(time)
                    # print('time remaining of current process =',current_procces.time_remaining)
                    queue.put(current_procces)
                    current_procces = queue.get()
                    current_procces.addMark(time)
                index = index + 1
        if current_procces == None:  # if the CPU is still empty from the begining
            time = round(time + 0.1, 1)  # just pass time and skip this iteration in the loop
            continue
        if current_procces.time_remaining <= 0:
            current_procces.addMark(time)
            if queue.isEmpty():
                break
            else:
                current_procces = queue.get()
                current_procces.addMark(time)
        current_procces.pass_time()  # let the current process
        time = round(time + 0.1, 1)

def RoundRobin(time_schedule, quantum):
    time = 0
    index = 0
    quant = quantum
    current_procces = None
    queue = SimpleQueue()

    while True:
        if index < len(time_schedule):
            if time >= time_schedule[index].arrival_time:
                new_process = time_schedule[index]
                if current_procces == None:
                    current_procces = new_process
                    current_procces.addMark(time)
                else:
                    queue.put(new_process)
                index = index + 1

        if current_procces == None:  # if the CPU is still empty from the begining
            time = round(time + 0.1, 1)  # just pass time and skip this iteration in the loop
            continue
        if current_procces.time_remaining <= 0:
            current_procces.addMark(time)
            if queue.isEmpty():
                break
            else:
                current_procces = queue.get()
                current_procces.addMark(time)
                quant = quantum

        if quant <= 0:
            current_procces.addMark(time)
            queue.put(current_procces)
            current_procces = queue.get()
            current_procces.addMark(time)
            quant = quantum

        current_procces.pass_time()
        time = round(time + 0.1, 1)
        quant = round(quant - 0.1, 1)

root = Tk()

root.title('Process Scheduler')
root.geometry("600x400")

time_schedule = []

processes_arrivals = []
processes_durations = []
processes_priorities = []

label_1 = Label(root, text='Enter number of processes : ')
label_1.grid(row=1, column=1)
entry = Entry(root)
entry.grid(row=1, column=2)

chosen_algorithm = StringVar()
chosen_algorithm.set('FCFS')
label_2 = Label(root, text='Scheduling Algorithm : ').grid(row=1, column=3)
drop = OptionMenu(root, chosen_algorithm, 'FCFS', 'SJF', 'SRTF', 'Round Robin').grid(row=1, column=4)

button = Button(root, text='Submit', command=lambda: manager(chosen_algorithm.get()))
button.grid(row=1, column=5)

def manager(algorithm):
    if algorithm == 'FCFS' or algorithm == 'SJF' or algorithm == 'SRTF':
        enter_processes_1(algorithm=algorithm)
    elif algorithm == 'Round Robin':
        enter_processes_2(algorithm=algorithm)

def build_schedule_1(algorithm):
    # build time_schedule for FCFS , SJF
    for i in range(len(processes_arrivals)):
        new_process = process(float(processes_arrivals[i].get()), float(processes_durations[i].get()), "P" + str(i))
        time_schedule.append(new_process)

    time_schedule.sort(key=lambda x: x.arrival_time)
    # print(algorithm)

    if algorithm == 'FCFS':
        FCFS(time_schedule=time_schedule)

    elif algorithm == 'SJF':
        SJF(time_schedule=time_schedule)

    elif algorithm == 'SRTF':
        SRTF(time_schedule=time_schedule)

    Plot(time_schedule=time_schedule)
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

def build_schedule_2(algorithm, quantum_entry):
    # build time_schedule for round robin
    quantum = float(quantum_entry.get())
    for i in range(len(processes_arrivals)):
        new_process = process(float(processes_arrivals[i].get()), float(processes_durations[i].get()), "P" + str(i))
        time_schedule.append(new_process)
    time_schedule.sort(key=lambda x: x.arrival_time)

    RoundRobin(time_schedule=time_schedule, quantum=quantum)
    Plot(time_schedule=time_schedule)
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

def enter_processes_1(algorithm):
    NumberOfProcesses = int(entry.get())
    label_II = Label(root, text="Enter Arrival Time").grid(row=2, column=1)
    label_III = Label(root, text="Enter Burst Time").grid(row=2, column=2)

    for i in range(NumberOfProcesses):
        label_I = Label(root, text="P" + str(i)).grid(row=i + 3, column=0)
        process_arrival = Entry(root)
        process_arrival.grid(row=i + 3, column=1)
        processes_duration = Entry(root)
        processes_duration.grid(row=i + 3, column=2)
        processes_arrivals.append(process_arrival)
        processes_durations.append(processes_duration)

    button_2 = Button(root, text="Gantt Chart", command=lambda: build_schedule_1(algorithm)).grid(row=3, column=3)

def enter_processes_2(algorithm):
    NumberOfProcesses = int(entry.get())

    label_II = Label(root, text="Enter arrival times").grid(row=2, column=1)
    label_III = Label(root, text="Enter Processes Durations").grid(row=2, column=2)
    label_V = Label(root, text='Quantum = ').grid(row=4, column=3)
    quantum_entry = Entry(root)
    quantum_entry.grid(row=4, column=4)

    for i in range(NumberOfProcesses):
        label_I = Label(root, text="P" + str(i)).grid(row=i + 3, column=0)
        process_arrival = Entry(root)
        process_arrival.grid(row=i + 3, column=1)
        processes_duration = Entry(root)
        processes_duration.grid(row=i + 3, column=2)
        processes_arrivals.append(process_arrival)
        processes_durations.append(processes_duration)

    button_2 = Button(root, text="Gantt Chart", command=lambda: build_schedule_2(algorithm, quantum_entry)).grid(row=3, column=3)

root.mainloop()