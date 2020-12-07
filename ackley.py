
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


class Ackley:

    def __init__(self, inf = -32, sup=32, step=0.25 ):
        self.__inf=inf
        self.__sup=sup
        self.__step=step

    def getInf(self):
        return self.__inf
    def getSup(self):
        return self.__sup
    def getStep(self):
        return self.__step

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

    def plot2d(self):
        X = np.arange(self.__inf, self.__sup, self.__step)
        Y = [self.ackley(np.array([x])) for x in X]
        plt.plot(X,Y)
        plt.show()

    def plot3d(self):

        X = np.arange(self.__inf, self.__sup, self.__step)
        Y = np.arange(self.__inf, self.__sup, self.__step)
        X, Y = np.meshgrid(X, Y)

        a = 20
        b = 0.2
        c = 2 * np.pi

        sum_sq_term = -a * np.exp(-b * np.sqrt(X*X + Y*Y) / 2)
        cos_term = -np.exp((np.cos(c*X) + np.cos(c*Y)) / 2)
        Z = a + np.exp(1) + sum_sq_term + cos_term

        fig = plt.figure()
        ax = plt.axes(projection='3d')

        ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        ax.set_title('Ackley plot')
        plt.show()


    def __del__(self):
        del self.__inf
        del self.__sup
        del self.__step