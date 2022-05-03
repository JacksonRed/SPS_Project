from ThreeDimensionPlot import Draw3D
from model import Model
storages=[7,10,14.5]
dutycycles=[0.1667,0.25,0.3333]


for storage in storages:
    for dutycycle in dutycycles:
        md=Model(storage,dutycycle)
        md.drawlowerbound()
        md.drawsystempower()
        #md.drawupperbound()
        md.adaptivedutycycle()
        md.modelAssemble()


draw=Draw3D()
draw.draw3Dplot()


