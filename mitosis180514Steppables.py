
from PySteppables import *
import CompuCell
import sys
from random import random
from PySteppablesExamples import MitosisSteppableBase
            

class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)
    def start(self):
        for cell in self.cellList:
            cell.targetVolume=25
            cell.lambdaVolume=2.0
        
        

class GrowthSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=1):
        SteppableBasePy.__init__(self,_simulator,_frequency)
    def step(self,mcs):
    #    for cell in self.cellList:
         #   cell.targetVolume+=1        
    # alternatively if you want to make growth a function of chemical concentration uncomment lines below and comment lines above        
        # field=CompuCell.getConcentrationField(self.simulator,"PUT_NAME_OF_CHEMICAL_FIELD_HERE")
        # pt=CompuCell.Point3D()
        field=CompuCell.getConcentrationField(self.simulator,"R") #####
        comPt=CompuCell.Point3D() #####
        
        for cell in self.cellList:
            if cell.type==self.P: #####
                comPt.x=int(cell.xCOM)
                comPt.y=int(cell.yCOM)
                comPt.z=int(cell.zCOM)
                concentrationAtCOM=field.get(comPt)
                cell.targetVolume+=0.01*concentrationAtCOM  # you can use here any fcn of concentrationAtCOM     
        
class MitosisData(object):
    def __init__(self, _MCS=-1, _parentId=-1, _parentType=-1, _offspringId=-1, _offspringType=-1):
        self.MCS=_MCS
        self.parentId=_parentId
        self.parentType=_parentType
        self.offspringId=_offspringId
        self.offspringType=_offspringType
    def __str__(self):
        return "Mitosis time="+str(self.MCS)+" parentId="+str(self.parentId)+"offspringId="+str(self.offspringId)
        

class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,_simulator,_frequency=1):
        MitosisSteppableBase.__init__(self,_simulator, _frequency)
    
    def step(self,mcs):
        # print "INSIDE MITOSIS STEPPABLE"
        cells_to_divide=[]
        for cell in self.cellList:
            if cell.volume>50:
                
                cells_to_divide.append(cell)
                
        for cell in cells_to_divide:
            # to change mitosis mode leave one of the below lines uncommented
            self.divideCellRandomOrientation(cell)
            # self.divideCellOrientationVectorBased(cell,1,0,0)                 # this is a valid option
            # self.divideCellAlongMajorAxis(cell)                               # this is a valid option
            # self.divideCellAlongMinorAxis(cell)                               # this is a valid option

    def updateAttributes(self):
        self.parentCell.targetVolume /= 2.0 # reducing parent target volume                 
        self.cloneParent2Child()            
        
        # for more control of what gets copied from parent to child use cloneAttributes function
        # self.cloneAttributes(sourceCell=self.parentCell, targetCell=self.childCell, no_clone_key_dict_list = [attrib1, attrib2] )
        
        if random()<0.5:
            self.childCell.type=self.parentCell.type
        else:
            self.childCell.type=self.DP

        parentCellList=[]
        parentCellList=CompuCell.getPyAttrib(self.parentCell)
        childCellList=[]
        childCellList=CompuCell.getPyAttrib(self.childCell)
        
        mcs=self.simulator.getStep()
        mitData=MitosisData(mcs,self.parentCell.id,self.parentCell.type,self.childCell.id,self.childCell.type)
        parentCellList.append(mitData)
        childCellList.append(mitData)
        