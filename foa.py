import sys
import random
from ackley import Ackley
import numpy as np


class FOA:
    def __init__(self, ackley=Ackley(), numSedds=30, maxTime=1000, dim=2, lifeTime=2, areaLimit=30, transferRate=5,
                 localSeeding=4, globalSeeding=3):
        self._ackley = ackley
        self._numSeeds = numSedds
        self._mAxTime = maxTime
        self._dim = dim
        self._lifeTime = lifeTime
        self._areLimit = areaLimit
        self._transferRate = transferRate
        self._localSeeding = localSeeding
        self._globalSeeding = globalSeeding
        self._trees = []
        self._candidate = []
        self._best = []
        self._notchange = 0
        for i in range(0, self._numSeeds):
            self._trees.append([])
            for j in range(0, self._dim):
                self._trees[i].append(random.uniform(self._ackley.getInf(), self._ackley.getSup()))
            self._trees[i].append(self.fitness(np.array(self._trees[i][0:self._dim].copy())))
            self._trees[i].append(0)

    def fitness(self, X):
        f_x = self._ackley.ackley(X)
        if f_x == 0:
            return sys.float_info.max
        return 1 / f_x;

    def localSeeding(self):
        new_trees = []
        for tree in self._trees:
            if tree[self._dim + 1] == 0:
                moveindex = [random.randrange(0, self._dim) for i in range(0, self._localSeeding)]
                for mi in moveindex:
                    trans = tree.copy()
                    trans[mi] = trans[mi] + random.uniform(-0.2, 2.0)
                    trans[self._dim] = self.fitness(np.array(trans[0:self._dim].copy()))
                    trans[self._dim + 1] = 0
                    new_trees.append(trans)
            tree[self._dim + 1] += 1

        for ntree in new_trees:
            self._trees.append(ntree)

    def controlForest(self):
        temp_tree = []
        for tree in self._trees:
            if tree[self._dim+1] <= self._lifeTime:
                temp_tree.append(tree)
            else:
                self._candidate.append(tree)
        if len(temp_tree) > self._areLimit:
            temp_tree.sort(key= lambda t:t[self._dim], reverse=True)
            while len(temp_tree) > self._areLimit:
                self._candidate.append(temp_tree.pop())
        self._trees.clear()
        for tree in temp_tree:
            self._trees.append(tree)


    def globalSeeding(self):
        selected_tree=[]
        while len(selected_tree) <= (len(self._candidate)*self._transferRate)/100:
            selected_tree.append(self._candidate.pop(random.randrange(0,len(self._candidate))))
        for tree in selected_tree:
            moveindex = [random.randrange(0, self._dim) for i in range(0, self._globalSeeding)]
            for mi in moveindex:
                trans = tree.copy()
                trans[mi] = random.uniform(self._ackley.getInf(), self._ackley.getSup())
                trans[self._dim] = self.fitness(np.array(trans[0:self._dim].copy()))
                trans[self._dim + 1] = 0
                self._trees.append(trans)
        self._candidate.clear()

    def updateBest(self):
        best_index=sys.maxsize
        besttone=sys.float_info.min
        for index in range(0, len(self._trees)):
            if self._trees[index][self._dim] > besttone:
                besttone=self._trees[index][self._dim]
                best_index=index
        temp_best=self._trees.pop(best_index)
        temp_best[self._dim+1]=0
        self._trees.insert(0,temp_best)
        if temp_best[self._dim] == self._best[self._dim]:
           self._notchange = self._notchange +1
        elif temp_best[self._dim] > self._best[self._dim]:
            self._notchange = 1
            self._best = temp_best.copy()
        else:
            print('some problem !!!!!!')

    def run(self):
        bestIndex = 0
        ackleyResult = 0
        bestIndex = random.randint(0, len(self._trees) - 1)
        self._best = self._trees[bestIndex]

        t = 0
        while t < self._mAxTime :
            print("##### The iteration number is:", t, " ##########")
            self.localSeeding()
            self.controlForest()
            self.globalSeeding()
            self.updateBest()
            print('############')
            t += 1
        ackleyResult = self.fitness(np.array(self._best[0:self._dim]))
        print('##### best result ######')
        print(self._best)
        print('################')

        print('##### ackleyResult is ##########')
        print(ackleyResult)
        print('################')
