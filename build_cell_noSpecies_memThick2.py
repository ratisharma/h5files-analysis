import sys
import os

if len(sys.argv) != 2:
    quit("Usage: output_filename")

outputFilename=sys.argv[1]

xlen=2.5e-6
ylen=2.5e-6
zlen=2.5e-6
latticeSpacing=50.0e-9
membraneThickness=100.0e-9
cellRadius=1.0e-6



builder=LatticeBuilder(xlen,ylen,zlen,latticeSpacing,1,0)
extraCellularType=0
extraCellular=Cuboid(point(0.0,0.0,0.0), point(xlen,ylen,zlen), extraCellularType)
builder.addRegion(extraCellular)
membraneType=1
center=point((xlen)/2.0,(ylen)/2.0,(ylen)/2.0)
membrane=CapsuleShell(center, center, cellRadius-membraneThickness, cellRadius, membraneType)
builder.addRegion(membrane)
cytoplasmType=2
cytoplasm=Capsule(center, center, cellRadius-membraneThickness, cytoplasmType)
builder.addRegion(cytoplasm)

# Species types.
L=0


# Make sure the file exists.
if not os.path.isfile(outputFilename):
    quit("Simulation file must already exist.")

# Open the file.
sim=SimulationFile(outputFilename)
spatialModel=SpatialModel()
builder.getSpatialModel(spatialModel)
sim.setSpatialModel(spatialModel)

# Discretize the lattice.
diffusionModel=DiffusionModel()
sim.getDiffusionModel(diffusionModel)
lattice = ByteLattice(diffusionModel.lattice_x_size(), diffusionModel.lattice_y_size(), diffusionModel.lattice_z_size(), diffusionModel.lattice_spacing(), diffusionModel.particles_per_site())
builder.discretizeTo(lattice, 0, 0.0)
sim.setDiffusionModel(diffusionModel)
sim.setDiffusionModelLattice(diffusionModel, lattice)

sim.close()

