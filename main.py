
from ackley import Ackley
from foa import FOA

foa=FOA(fun=Ackley(2,-5,5,0.05,'contour'),numSedds=30, maxTime=1000, lifeTime=2, areaLimit=30, localMotion=0.01, localSeeding=4,transferRate=4, globalSeeding=2)
foa.run()

#foa=FOA(fun=Ackley(2,-5,5,0.05,'3d'),numSedds=30, maxTime=100, lifeTime=2, areaLimit=30, localMotion=0.1, localSeeding=4,transferRate=4, globalSeeding=2)
#foa.run()

#foa=FOA(fun=Ackley(1,-5,5,0.05,'2d'),numSedds=30, maxTime=100, lifeTime=2, areaLimit=30, localMotion=0.01, localSeeding=4,transferRate=3, globalSeeding=2)
#foa.run()