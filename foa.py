import random
import sys

import numpy as np

from ackley import Ackley


class FOA:
    def __init__(self, fun=Ackley(), numSedds=30, maxTime=1000, lifeTime=2, areaLimit=30, localMotion=0.1, localSeeding=4,transferRate=4, globalSeeding=2):
        self._fun = fun
        self._numSeeds = numSedds
        self._mAxTime = maxTime
        self._dim = self._fun.getDim()
        self._lifeTime = lifeTime
        self._areLimit = areaLimit
        self._transferRate = transferRate
        self._localMotion = localMotion
        self._localSeeding = localSeeding
        self._globalSeeding = globalSeeding
        self._trees = []
        self._candidate = []
        self._best = []
        self._notchange = 0
        for i in range(0, self._numSeeds):
            self._trees.append([])
            for j in range(0, self._dim):
                self._trees[i].append(random.uniform(self._fun.getInf(), self._fun.getSup()))
            self._trees[i].append(self._fun.fitness(np.array(self._trees[i][0:self._dim].copy())))
            self._trees[i].append(0)

    def localSeeding(self):
        new_trees = []
        for tree in self._trees:
            if tree[self._dim + 1] == 0:
                moveindex = [random.randrange(0, self._dim) for i in range(0, self._localSeeding)]
                for mi in moveindex:
                    trans = tree.copy()
                    trans[mi] = trans[mi] + random.uniform(-1*self._localMotion, self._localMotion)
                    trans[self._dim] = self._fun.fitness(np.array(trans[0:self._dim].copy()))
                    trans[self._dim + 1] = 0
                    new_trees.append(trans)
            tree[self._dim + 1] += 1

        for ntree in new_trees:
            self._trees.append(ntree)

    def controlForest(self):
        temp_tree = []
        for tree in self._trees:
            if tree[self._dim + 1] <= self._lifeTime:
                temp_tree.append(tree)
            else:
                self._candidate.append(tree)
        if len(temp_tree) > self._areLimit:
            temp_tree.sort(key=lambda t: t[self._dim], reverse=True)
            while len(temp_tree) > self._areLimit:
                self._candidate.append(temp_tree.pop())
        self._trees.clear()
        for tree in temp_tree:
            self._trees.append(tree)

    def globalSeeding(self):
        selected_tree = []
        while len(selected_tree) <= (len(self._candidate) * self._transferRate) / 100:
            selected_tree.append(self._candidate.pop(random.randrange(0, len(self._candidate))))
        for tree in selected_tree:
            moveindex =[]
            while len(moveindex) < self._globalSeeding:
                r=random.randrange(0, self._dim)
                if r not in moveindex: moveindex.append(r)
            trans = tree.copy()
            for mi in moveindex:
                trans[mi] = random.uniform(self._fun.getInf(), self._fun.getSup())
            trans[self._dim] = self._fun.fitness(np.array(trans[0:self._dim].copy()))
            trans[self._dim + 1] = 0
            self._trees.append(trans)
        self._candidate.clear()

    def updateBest(self):
        best_index = sys.maxsize
        besttone = sys.float_info.min
        for index in range(0, len(self._trees)):
            if self._trees[index][self._dim] > besttone:
                besttone = self._trees[index][self._dim]
                best_index = index
        temp_best = self._trees.pop(best_index)
        temp_best[self._dim + 1] = 0
        self._trees.insert(0, temp_best)
        if temp_best[self._dim] == self._best[self._dim]:
            self._notchange = self._notchange + 1
        elif temp_best[self._dim] > self._best[self._dim]:
            self._notchange = 1
            self._best = temp_best.copy()
        else:
            print('some problem !!!!!!')

    def run(self):
        bestIndex = random.randint(0, len(self._trees) - 1)
        self._best = self._trees[bestIndex]


        animate = getattr(self._fun, "animate", None)
        if callable(animate) and self._dim <= 2:
            self._fun.animate(self._mAxTime,self.update)
        else:
            t = 0
            while t < self._mAxTime:
                self.update(t,)
                t += 1

        ackleyResult = self._fun.fitnessG(np.array(self._best[0:self._dim]))
        print('##### best result ######')
        print(self._best)
        print('################')
        print('##### result is ##########')
        print(ackleyResult)
        print('################')

    def update(self,i, scat):
        print("##### The iteration number is:", i, " ##########")
        self.localSeeding()
        self.controlForest()
        self.globalSeeding()
        self.updateBest()
        if scat and self._fun.getAnimType()=='3d':
            xdata = [tree[0] for tree in self._trees]
            ydata = [tree[1] for tree in self._trees]
            zdata = [self._fun.fitnessG(np.array([tree[0],tree[1]])) for tree in self._trees]
            scat._offsets3d=(xdata, ydata, zdata)

        if scat and self._fun.getAnimType()=='contour':
            xdata = [tree[0] for tree in self._trees]
            ydata = [tree[1] for tree in self._trees]
            scat.set_data(xdata, ydata)

        if scat and self._fun.getAnimType()=='2d':
            xdata = [tree[0] for tree in self._trees]
            ydata = [self._fun.fitnessG(np.array([tree[0]])) for tree in self._trees]
            scat.set_data(xdata, ydata)

        print('##### best result ######')
        print(self._best)
        print(self._fun.fitnessG(np.array(self._best[0:self._dim])))
        print('############')