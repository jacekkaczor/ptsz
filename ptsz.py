import math
import time as times

paths = {10: "sch10.txt", 20: "sch20.txt", 50: "sch50.txt", 100: "sch100.txt", 200: "sch200.txt", 500: "sch500.txt",
         1000: "sch1000.txt"}
work = 0


class Task:
    def __init__(self, ID, p, a, b):
        self.ID = ID
        self.p = p
        self.a = a
        self.b = b

    def __lt__(self, other):
        if (self.a == other.a):
            return (self.b > other.b)
        else:
            return (self.a < other.a)

    def __str__(self):
        return str(self.ID)


class Instance:
    h = 0.0
    result = 0
    schedule = []
    optimal_schedule = []
    optimal_result = 0
    r = 0  # offset
    time = 0
    duration = 0
    size = 0

    def __init__(self, k, n, h):
        self.tasks = []
        self.k = k
        self.n = n
        self.h = h
        self.working_time = work

    def pSum(self):
        pSum = 0
        for task in self.tasks:
            pSum += task.p
        return pSum

    def pMax(self):
        self.tasks.sort(key=lambda task: task.p, reverse=True)
        self.max = self.tasks[0].p
        print("MAX: ", self.max)

    def calculate_d(self):
        self.d = math.floor(self.pSum() * self.h)

    def saveInstance(self):
        text = ""
        with open("./wyniki/moje/" + str(self) + '.txt', 'w') as file:
            text += str(self.optimal_result) + ' '
            text += str(self.h) + ' '
            text += str(self.r) + ' '
            for task in self.optimal_schedule:
                text += str(task) + ' '
            file.write(text)

    def calculate_result(self, schedule, r):
        result = 0
        time = 0 + r
        for task in schedule:
            time += task.p
            result += max(self.d - time, 0) * task.a
            result += max(time - self.d, 0) * task.b
        return result

    def first_calculate(self):
        self.calculate_d()
        schedule = []
        r = 0
        time = 0
        tasks = self.tasks[:]
        tasks.sort()
        reverse = True
        for i in range(len(tasks)):
            if time > 0.8 * self.d and reverse:
                tasks.sort(key=lambda task: task.b, reverse=True)
                reverse = False
            task = tasks[0]
            tasks.remove(task)
            schedule.append(task)
            time += task.p
        self.optimal_result = self.calculate_result(schedule, r)
        self.optimal_schedule = schedule[:]
        print(self.optimal_result)

    def calculate(self, schedule, time, r, tasks):
        self.duration = times.perf_counter() - self.start
        if self.duration > self.working_time:
            return 0
        if time > 0.8 * self.d:
            tasks.sort(key=lambda task: task.b, reverse=True)
        else:
            tasks.sort()
        for task in tasks:
            schedule.append(task)
            time += task.p
            result = self.calculate_result(schedule, r)
            tasks2 = tasks[:]
            tasks2.remove(task)
            if time > self.d + 2 * self.max + 1:
                schedule.extend(tasks2)
                result = self.calculate_result(schedule, r)
                if result < self.optimal_result:
                    self.optimal_result = result
                    self.optimal_schedule = schedule[:]
                    self.r = r
                return 1
            else:
                if result >= self.optimal_result:
                    return 1
                else:
                    if len(schedule) == self.n:
                        self.optimal_result = result
                        self.optimal_schedule = schedule[:]
                        self.r = r
                if self.calculate(schedule[:], time, r, tasks2) == 0:
                    return 0
            schedule.remove(task)
        return 1

    def calculate_schedule(self):
        self.start = times.perf_counter()
        self.first_calculate()
        self.duration = times.perf_counter() - self.start
        r = 0
        maxR = self.d
        self.pMax()
        while self.duration < self.working_time and r < maxR:
            self.calculate([], 0, r, self.tasks[:])
            self.duration = times.perf_counter() - self.start
            r += 1
        print("last r: ", r - 1)
        print("time: ", self.duration)

    def check_result(self):
        self.calculate_d()
        result = 0
        time = 0 + self.r
        if not len(self.schedule) == self.n:
            return "incorrect"
        for task in self.schedule:
            time += task.p
            result += max(self.d - time, 0) * task.a
            result += max(time - self.d, 0) * task.b
        print("Result: ", result)
        return "correct" if self.result == result else "incorrect"

    def print_result(self):
        text = ""
        for task in self.schedule:
            text += str(task) + " "

    def __str__(self):
        return 'n' + str(self.n) + 'k' + str(self.k) + 'h' + str(self.h)[2]


def loadInstances(path):
    instances = []
    with open(path) as file:
        content = file.readlines()
    content = [x.strip().split() for x in content]
    content = content[1:]
    n, k, ID = 0, 1, 0
    for line in content:
        if (len(line) == 1):
            n = int(line[0])
            instance = Instance(k, n, h)
            k += 1
            ID = 0
        else:
            instance.tasks.append(Task(ID, int(line[0]), int(line[1]), int(line[2])))
            ID += 1
            if (len(instance.tasks) == n - 1):
                instances.append(instance)
    return instances


def checkResult(path):
    file = path.split('/')[-1]
    n = int(file[1:file.index('k')])
    k = int(file[file.index('k') + 1:file.index('h')])
    h = float("0." + file[file.index('h') + 1:file.index('.')])
    instance = loadInstances(paths[n])[k - 1]
    with open("./wyniki/" + path) as f:
        content = f.readline().split()
    instance.result = int(content[0])
    instance.h = float(content[1])
    instance.r = int(content[2])
    for ID in content[3:]:
        instance.schedule.append(instance.tasks[int(ID)])
    print(file, instance.check_result())


def calculate():
    instances = loadInstances(paths[n])
    instance = instances[k - 1]
    instance.calculate_schedule()
    instance.saveInstance()
    checkResult("moje/" + str(instance) + ".txt")


k = 2
h = 0.8
n = 10
work = 10

calculate()