
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation

import sys

global anim

class Ackley:

    def __init__(self, dim = 2, inf = -32, sup=32, step=0.25 , anim_type='3d' ):
        self.__inf=inf
        self.__sup=sup
        self.__step=step
        self.__dim = dim
        self.__anim_type=anim_type

    def getInf(self):
        return self.__inf
    def getSup(self):
        return self.__sup
    def getStep(self):
        return self.__step
    def getDim(self):
        return self.__dim
    def getAnimType(self):
        return self.__anim_type

    def ackley(self,x):

        a = 20
        b = 0.2
        c = 2 * np.pi
        d= len(x)

        sum_sq_term = -a * np.exp(-b * np.sqrt(sum(x*x) / d))
        cos_term = -np.exp(sum(np.cos(c*x) / d))
        y = a + np.exp(1) + sum_sq_term + cos_term

        del a,b,c,sum_sq_term,cos_term
        return y

    def animatePlot2(self,maxtime,update):
        global anim

        X = np.arange(self.__inf, self.__sup, self.__step)
        Y = [self.ackley(np.array([x])) for x in X]

        self.__fig, self.__ax = plt.subplots()

        plt.plot(X,Y)

        scat, =self.__ax.plot([], [], 'k.',marker='x', markersize=5)

        anim=matplotlib.animation.FuncAnimation(self.__fig, update, frames=maxtime,repeat=False,fargs=(scat,))

        plt.show()

    def animatePlotContour(self,maxtime,update):
        global anim
        X = np.arange(self.__inf, self.__sup, self.__step)
        Y = np.arange(self.__inf, self.__sup, self.__step)
        X, Y = np.meshgrid(X, Y)

        a = 20
        b = 0.2
        c = 2 * np.pi

        sum_sq_term = -a * np.exp(-b * np.sqrt(X*X + Y*Y) / 2)
        cos_term = -np.exp((np.cos(c*X) + np.cos(c*Y)) / 2)
        Z = a + np.exp(1) + sum_sq_term + cos_term

        self.__fig, self.__ax = plt.subplots()

        plt.contourf(X, Y, Z)

        scat, =self.__ax.plot([], [], 'k.',marker='x', markersize=5)

        anim=matplotlib.animation.FuncAnimation(self.__fig, update, frames=maxtime,repeat=False,fargs=(scat,))

        plt.show()

    def animatePlot3(self,maxtime,update):
        global anim
        self.__fig = plt.figure()
        self.__ax = plt.axes(projection='3d')
        self.__ax.view_init(60, 35)

        X = np.arange(self.__inf, self.__sup, self.__step)
        Y = np.arange(self.__inf, self.__sup, self.__step)
        X, Y = np.meshgrid(X, Y)

        a = 20
        b = 0.2
        c = 2 * np.pi

        sum_sq_term = -a * np.exp(-b * np.sqrt(X*X + Y*Y) / 2)
        cos_term = -np.exp((np.cos(c*X) + np.cos(c*Y)) / 2)
        Z = a + np.exp(1) + sum_sq_term + cos_term

        self.__ax.plot_surface(X, Y, Z,cmap=cm.coolwarm, linewidth=0, alpha = 0.5, edgecolor = 'k')

        scat =self.__ax.scatter([], [], [],marker='x',s=20,alpha = 1)

        anim=matplotlib.animation.FuncAnimation(self.__fig, update, frames=maxtime,repeat=False,fargs=(scat,))

        plt.show()

    def fitness(self, X):
        f_x = self.ackley(X)
        if f_x == 0:
            return sys.float_info.max
        return 1 / f_x

    def fitnessG(self, X):
        return self.ackley(X)

    def animate(self,maxtime,update):
       if self.__anim_type == '2d':
           self.animatePlot2(maxtime,update)
       if self.__anim_type == '3d':
           self.animatePlot3(maxtime,update)
       if self.__anim_type == 'contour':
           self.animatePlotContour(maxtime,update)

    def save_animate(self):
        anim.save('ackley.gif', writer = 'PillowWriter', fps=15)

    def __del__(self):
        del self.__inf
        del self.__sup
        del self.__step
