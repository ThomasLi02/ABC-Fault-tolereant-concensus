import random
import math
import matplotlib.pyplot as plt


class System:
   def __init__(self, maxByz):
       self.processors = []
       self.r = 1
       self.p = 0.01
       n = maxByz*3
       self.maxByz = int(maxByz)
       t = int(self.maxByz)
       c = (n - 2*t - 1)/t + 1
       self.termRound = math.log((1.0/0.001), c)
       self.attack = 0


class Node:
   def __init__(self, status, round, queue, roundFault):
       self.status = float(status)
       self.round = int(round)
       self.queue = queue
       self.roundFault = roundFault
       self.isByz = False

# takes in a System and sees if the processors are in agreement
def inAgreement(S):
   maxState = 0
   minState = 1
   for i in range(len(S.processors)):
       if not S.processors[i].isByz:
           if S.processors[i].status < minState:
               minState = S.processors[i].status
           if S.processors[i].status > maxState:
               maxState = S.processors[i].status
   return maxState - minState <=0.0001




# puts node in the message queue of all processors in system
def send(node, S):
   if not node.isByz:
       for k in range(len(S.processors)):
           if not S.processors[k].isByz:  #if node is not Byz, send status to all non-Byzn nodes
               S.processors[k].queue.append(node.status)
   else:
       for k in range(len(S.processors)):
           if not S.processors[k].isByz: #if node is Byz, send random value to all non-Byzn nodes
               if S.attack == 0:
                   randomAttack(k,S)
               if S.attack == 1:
                   worstAttack(k,S)


def worstAttack(k,S):
    if S.processors[k].status >= 0.5:
        S.processors[k].queue.append(1)
    else:
        S.processors[k].queue.append(0)

def randomAttack(k,S):
    S.processors[k].queue.append(random.random())


def receive(node, S):
    i = 0
    while i < (len(node.queue)):
       if random.random() < S.p: #probability p a message is lost
           node.queue[i] = node.status  #if loss, replace with receiver status
       i += 1
    node.queue.sort() #sort the message queue

def run(S):
   for x in range(len(S.processors)):
       if S.processors[x].roundFault == S.r: #node becomes Byz if its fault round == round
           S.processors[x].isByz = True
   for i in range(len(S.processors)):  # each node sends message to all processors
       send(S.processors[i], S)
   for j in range(len(S.processors)):  # non Byz nodes receive messages
       if not S.processors[j].isByz:
           receive(S.processors[j], S)
       S.processors[j].round = S.processors[j].round + 1 #increment all nodes' round
   for k in range(len(S.processors)):
       if not S.processors[k].isByz:
           sum = 0
           bottom = S.processors[k].queue[int(S.maxByz) - 1] #discarding bottom f
           z= len(S.processors[k].queue) - S.maxByz-1 #discarding topf
           top =S.processors[k].queue[int(z)]
           sum = sum + bottom + top
           ave = sum/2
           S.processors[k].status = ave
       del S.processors[k].queue[:] #clear all queues
   S.r += 1
   if not inAgreement(S) and not S.r == S.termRound:  # run again if the processors are not in agreement
       run(S)



#n vs. round converge
def go():

    ticks = []
    BF = [15,30,50,75,125,250]
    for i in range(6):
        ticks.append(i+1)
    replaceTicks = []
    data = []

    for j in range(6):
        dataPerConfig = []
        mySystem = System((BF[j]*(1.0/3)))
        mySystem.p = 0.05
        messageLost = mySystem.p
        replaceTicks.append(BF[j])
        for k in range(100):
            for z in range(BF[j]):
                if random.random()<0.5:
                    x = 1
                else:
                    x = 0
                if z < BF[j]*(1.0/3)-1:
                    processor = Node(x, 1, [], 1)
                else:
                    processor = Node(x, 1, [], 500)
                mySystem.processors.append(processor)
            run(mySystem)

            dataPerConfig.append(mySystem.r)
            mySystem = System(BF[j]*(1.0/3))
            mySystem.p = messageLost
        data.append(dataPerConfig)

    print(ticks)
    print(replaceTicks)
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.boxplot(data)
    plt.xticks(ticks, replaceTicks)

    plt.xlabel('n')
    plt.ylabel('Round Converge')
    plt.ylim(0)
    plt.savefig("nVarRand.pdf")

    plt.show()


#message loss rate vs round convergee
def go1():
    ticks = []
    BF = [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4]
    for i in range(8):
        ticks.append(i+1)
    replaceTicks = []
    data = []

    for j in range(8):
        dataPerConfig = []
        mySystem = System((50*(1.0/3)))
        mySystem.p =BF[j]
        messageLost = mySystem.p
        replaceTicks.append(BF[j])
        for k in range(100):
            for z in range(50):
                if random.random()<0.5:
                    x = 1
                else:
                    x = 0
                if z < 50*(1.0/3)-1:
                    processor = Node(x, 1, [], 1)
                else:
                    processor = Node(x, 1, [], 500)
                mySystem.processors.append(processor)
            run(mySystem)

            dataPerConfig.append(mySystem.r)
            mySystem = System(50*(1.0/3))
            mySystem.p = messageLost
        data.append(dataPerConfig)

    print(ticks)
    print(replaceTicks)
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.boxplot(data)
    plt.xticks(ticks, replaceTicks)

    plt.xlabel('Message loss-rate')
    plt.ylabel('Round Converge')
    plt.ylim(0)
    plt.savefig("lossRateVarRand.pdf")

    plt.show()


# message loss-rate vs % runs with inconclusive outputs
def go2():
    ticks = []
    BF = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    BFstr = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6']

    for i in range(6):
        ticks.append(i + 1)
    replaceTicks = []
    data = []

    for j in range(6):
        mySystem = System((50 * (1.0 / 3)))
        mySystem.p = BF[j]
        messageLost = mySystem.p
        replaceTicks.append(BF[j])
        inconclusive = 0
        print(mySystem.p)
        for k in range(100):
            count = 0
            for z in range(50):
                if count < (int(0.5*(50 * (2.0 / 3))+0.5)):
                    x = 1
                else:
                    x = 0
                if z < 50 * (1.0 / 3):
                    processor = Node(x, 1, [], 1)
                else:
                    processor = Node(x, 1, [], 25)
                    count += 1
                mySystem.processors.append(processor)


            run(mySystem)
            for g in range(len(mySystem.processors)):
                if 0.5-0.001/2 <= mySystem.processors[g].status <= 0.5+0.001/2:
                    inconclusive += 1
                    break
            mySystem = System(50 * (1.0 / 3))
            mySystem.p = messageLost
        data.append(inconclusive)

    print(ticks)
    print(replaceTicks)
    print(data)
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    plt.bar(BFstr, data)
    plt.xlabel('message loss-rate')
    plt.ylabel('% runs with inconclusive outputs')
    plt.ylim(0)
    plt.savefig("thirdplot.pdf")
    plt.show()





go2()





