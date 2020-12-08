
from ackley import Ackley
from foa import FOA

foa=FOA(ackley=Ackley(-15,15,0.25))
foa.run()