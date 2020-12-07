
from ackley import Ackley
from foa import FOA

ack=Ackley(-15,15,0.01)
ack.plot2d()

foa=FOA()
foa.run()