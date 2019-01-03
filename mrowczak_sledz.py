import math
import time as times
import numpy as np
import random

paths = {10: "sch10.txt", 20: "sch20.txt", 50: "sch50.txt", 100: "sch100.txt", 200: "sch200.txt", 500: "sch500.txt",
         1000: "sch1000.txt"}
work = 0

alpha = 1
beta = 0
ro = 0.01

def normalizate(d):
    # d is a (n x dimension) np array
    d -= np.min(d, axis=0)
    d /= np.ptp(d, axis=0)
    su = np.sum(d)
    d /= su
    return d





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

    def __str__(self):
        return str(self.ID)

class Ant:
    def __init__(self):
        self.schedule = []
        self.result = 0
        self.r = 0

    def __lt__(self, other):
        return self.result < other.result

class Instance:
    h = 0.0
    result = 0
    schedule = []
    r = 0  # offset
    time = 0
    duration = 0
    start = 0
    d = 0
    
    
    def __init__(self, k, n, h):
        self.tasks = []
        self.k = k
        self.n = n
        self.h = h
        self.pheromoneR = []
        self.pheromone = []
        #moje_start
        self.pheromone_start = [] 
        #moje_stop
        self.working_time = work

        

    def pSum(self):
        pSum = 0
        for task in self.tasks:
            pSum += task.p
        return pSum

    def calculate_d(self):
        self.d = math.floor(self.pSum() * self.h)

    def saveInstance(self):
        text = ""
        with open("./wyniki/moje/" + str(self) + '.txt', 'w') as file:
            text += str(self.result) + ' '
            text += str(self.h) + ' '
            text += str(self.r) + ' '
            for task in self.schedule:
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
        self.result = self.calculate_result(schedule, r)
        self.schedule = schedule[:]
        print("First: ", self.result)


    def update_pheromone(self,schedule):
        for i in range(self.n-1):

            self.pheromone[schedule[i].ID,schedule[i+1].ID] += 1

    def update_pheromones(self,ant):
        res = ant.result
        value_added = (1/res)
        self.pheromoneR[ant.r] = self.pheromoneR[ant.r] + value_added
        self.pheromone_start[ant.schedule[0].ID] =  self.pheromone_start[ant.schedule[0].ID]  + value_added
        for i in range(self.n-1):
            self.pheromone[ant.schedule[i].ID,ant.schedule[i+1].ID] = self.pheromone[ant.schedule[i].ID,ant.schedule[i+1].ID] + value_added


    def vapo_pheromones(self):
        self.pheromone *= (1-ro)
        self.pheromone_start *= (1-ro)
        self.pheromoneR *= (1-ro)

    def initial_colony(self, size):
        colony = []
        self.colony_size = size
        for _ in range(size):
            ant = Ant()
            ant.r = random.randrange(self.d+1)
            tasks = self.tasks[:]
            for _ in range(self.n):
                task = tasks.pop(random.randrange(len(tasks)))
                ant.schedule.append(task)
            ant.result = self.calculate_result(ant.schedule, ant.r)
            colony.append(ant)
        colony.sort()
        self.compare_new_result(colony[0].result,colony[0].r,colony[0].schedule)
        self.vapo_pheromones()
        for ant in range(int(size/5)):
            self.update_pheromones(colony[ant]) 
        return colony
    

    def compare_new_result(self,result,r,schedule):
        if(result<self.result):
            self.result = result
            self.r = r 
            self.schedule = schedule[:]

    def choose_next_task(self,tasks,id):
        temp_pheromone = self.pheromone[id][:]
        curr_pheromone = []
        tasks_ids = [x.ID for x in tasks]
        for task in tasks_ids:
            curr_pheromone.append(temp_pheromone[task])
        curr_pheromone=normalizate(curr_pheromone)
        next_id = np.random.choice(tasks_ids,p=curr_pheromone)
        return next_id



    def calculate_all_colonies(self,G,size):
        
        for g in range(G):
            colony = []
            for _ in range(size):
                r_s = np.arange(self.d)
                task_s = np.arange(self.n)
                ant = Ant()
                prob_r = normalizate(self.pheromoneR)
                ant.r = np.random.choice(r_s,p=prob_r)
                tasks = self.tasks[:]
                task_prob = normalizate(self.pheromone_start)
                last_id = np.random.choice(task_s,p=task_prob)
                start = tasks[last_id]
                ant.schedule.append(start)
                tasks.remove(start)
                task_s = np.delete(task_s,last_id)
                while(len(tasks)>1):
                    last_id = self.choose_next_task(tasks,last_id)
                    curr_task = [x for x in tasks if x.ID == last_id]
                    curr_task = curr_task[0]
                    ant.schedule.append(curr_task)
                    tasks.remove(curr_task)
                
                curr_task = tasks.pop(0)
                ant.schedule.append(curr_task)
                ant.result = self.calculate_result(ant.schedule,ant.r)

                colony.append(ant)
            colony.sort()
            self.compare_new_result(colony[0].result,colony[0].r,colony[0].schedule)
            self.vapo_pheromones()
            for ant in range(int(size/3)):
                self.update_pheromones(colony[ant])











    def calculate_schedule(self):
        self.start = times.perf_counter()
        self.first_calculate()
        self.tasks.sort(key=lambda task: task.ID)
        m = 100  # size of colony
        G = 10000
        self.pheromoneR = np.ones(self.d)
        self.pheromone = np.ones((self.n, self.n))
        self.pheromone_start = np.ones((self.n))

        self.pheromone_start *= 1/self.result
        self.pheromoneR *= 1/self.result
        self.pheromone *= 1/self.result


        self.initial_colony(m)
        self.calculate_all_colonies(G,m)

        print(self.pheromone)
        self.duration = times.perf_counter() - self.start
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
        print("R: ",self.r)
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


k = 9
h = 0.6
n = 10
work = 10   

calculate()
