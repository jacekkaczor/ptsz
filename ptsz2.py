import math
import random
import time

paths = {10: "sch10.txt", 20: "sch20.txt", 50: "sch50.txt", 100: "sch100.txt", 200: "sch200.txt", 500: "sch500.txt",
         1000: "sch1000.txt"}


class Task:
    def __init__(self, ID, p, a, b):
        self.ID = ID
        self.p = p
        self.a = a
        self.b = b

    def __lt__(self, other):
        if self.a == other.a:
            return self.b > other.b
        else:
            return self.a < other.a

    def __gt__(self, other):
        if self.b == other.b:
            return self.a < other.a
        else:
            return self.b > other.b

    def __str__(self):
        return str(self.ID)


class Instance:
    h = 0.0
    result = 0
    schedule = []
    r = 0  # offset
    time = 0
    optimal_schedule = []
    optimal_result = float('inf')

    def __init__(self, k, n, h):
        self.tasks = []
        self.k = k
        self.n = n
        self.h = h

    def pSum(self):
        pSum = 0
        for task in self.tasks:
            pSum += task.p
        return pSum

    def calculate_d(self):
        self.d = math.floor(self.pSum() * self.h)

    def calculate_result(self, schedule, r):
        result = 0
        time = 0 + r
        for task in schedule:
            time += task.p
            result += max(self.d - time, 0) * task.a
            result += max(time - self.d, 0) * task.b
        return result

    def saveInstance(self):
        text = ""
        with open("./wyniki/moje/" + str(self) + '.txt', 'w') as file:
            text += str(self.optimal_result) + ' '
            text += str(self.h) + ' '
            text += str(self.r) + ' '
            for task in self.optimal_schedule:
                text += str(task) + ' '
            file.write(text)

    def first_calculate(self):
        self.calculate_d()
        schedule = []
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
        maxR = self.d * 1.1
        for r in range(int(maxR)):
            result = self.calculate_result(schedule, r)
            if r == 0:
                print("FIRST = ", result)
            self.compare_new_result(result, r, schedule)

    def calculate_schedule(self, key):
        self.calculate_d()
        schedule = []
        time = 0
        tasks = self.tasks[:]
        tasks.sort(key=key[0], reverse=key[1])
        stop = 0.8 * self.d
        while time < stop:
            task = tasks[0]
            tasks.remove(task)
            schedule.append(task)
            time += task.p
        task = False
        while time < self.d:
            for t in tasks:
                if t.p + time < self.d:
                    task = t
                    break
            if not task:
                break
            tasks.remove(task)
            schedule.append(task)
            time += task.p
            task = False
        tasks.sort(key=lambda t: t.b, reverse=True)
        schedule.extend(tasks)
        maxR = self.d * 1.1
        for r in range(int(maxR)):
            result = self.calculate_result(schedule, r)
            self.compare_new_result(result, r, schedule)

    def swap(self):
        for _ in range(n):
            sch = self.optimal_schedule[:]
            self.swap_random(sch)
            result = self.calculate_result(sch, self.r)
            self.compare_new_result(result, self.r, sch)
            # if self.compare_new_result(result, self.r, sch):
                # print("    ", result)
                # for i in range(int(self.d/5)):
                #     if self.r-i >= 0:
                #         if self.compare_new_result(result, self.r-i, sch):
                #             print("rrrrrrrrrr", result)
                #     if self.compare_new_result(result, self.r+i, sch):
                #         print("rrrrrrrrrrrr", result)

    def swap_random(self, seq):
        idx = range(len(seq))
        i1, i2 = random.sample(idx, 2)
        seq[i1], seq[i2] = seq[i2], seq[i1]

    def compare_new_result(self, result, r, schedule):
        if result < self.optimal_result:
            self.optimal_result = result
            self.optimal_schedule = schedule[:]
            self.r = r
            print(result)
            return True
        return False

    def check_result(self):
        self.calculate_d()
        result = 0
        time = 0 + self.r
        for task in self.schedule:
            time += task.p
            result += max(self.d - time, 0) * task.a
            result += max(time - self.d, 0) * task.b
        print(result)
        return "correct" if self.result == result else "incorrect"

    def print_result(self, schedule):
        text = ""
        for task in schedule:
            text += str(task) + " "
        print(text)

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
    start = time.perf_counter()
    instance.calculate_d()
    instance.first_calculate()
    keys = [[lambda x: (x.b-x.a, x.p), True], [lambda x: (x.a-x.b)/x.p, True], [lambda x: x.b-x.a-x.p, True]]
    for key in keys:
        print("Key = ", keys.index(key))
        instance.calculate_schedule(key=key)
    for _ in range(100):
        instance.swap()
    duration = time.perf_counter() - start
    print(str(instance))  # , instance.result, instance.schedule)
    print("Time = ", duration)
    print('d = ', instance.d)
    print('r = ', instance.r)
    instance.saveInstance()
    checkResult("moje/" + str(instance) + ".txt")


k = 1
h = 0.2
n = 10

calculate()
# checkResult("n10k1h2.txt")
