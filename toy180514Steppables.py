
from PySteppables import *
import CompuCell
import sys
class toy180514Steppable(SteppableBasePy):

    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)
    def start(self):
        pass
        # any code in the start function runs before MCS=0
        #print "CELLTYPE=",self.P
        #print "CELLTYPE=",self.N
#        else:
#            pass
    def step(self,mcs):        
        pass
        #type here the code that will run every _frequency MCS
        #for cell in self.cellList:
            
            #print "cell.id=",cell.id
    def finish(self):
        # Finish Function gets called after the last MCS
        for cell in self.cellList:
            print "cell volume = ", cell.volume
        