
from ackley import Ackley
from foa import FOA

foa=FOA(ackley=Ackley(-300,300,0.25))
foa.run()