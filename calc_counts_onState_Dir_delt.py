import datetime
import os
import sys
from os import listdir
from numpy import *
import h5py
from robertslab.cellio import *

if len(sys.argv) < 7:
    print "Usage: calc_rdme_pdf.py output_dir inputFile species onThreshold finalTime i [j k l m ...]"
    quit()

outputDir=sys.argv[1]
inputFile=sys.argv[2]
species=int(sys.argv[3])
onThreshold=int(sys.argv[4])
finalTime=int(sys.argv[5])
indices=()
for i in range(6,len(sys.argv)):
    indices+=(int(sys.argv[i]),)

# Create the arrays to store the stats.
Xtot=arange(0,1)
Ctot=zeros(1,dtype=int32)

# Create an array for the counts.
lattice=zeros((50,50,50,16))
latticeShape=lattice.shape
#counts=zeros(latticeShape)
counts=zeros((latticeShape[0],latticeShape[1],latticeShape[2],latticeShape[3]+1))
countsShape=counts.shape
print("Created empty array for counts: %s"%(counts.shape,))
Lcount=0

#inputFiles=os.listdir( Dirpath )
#print("Processing inputfiles")
#print("Processing %d files"%(len(inputFiles)))
#for iFile in inputFiles:
# Load the file.
    #print("Loading %s"%(iFile));
    #iFile2=os.path.join(Dirpath,iFile)
    #print("Processing %s"%(iFile2))
f=h5py.File(inputFile, 'r')
    
print("Processing %s file"%(inputFile))

# Get the list of replicates.
Rs=list(f["/Simulations"])
    #Rs=[1]
print("Processing %d replicates"%(len(Rs)))

    # Go through each replicate.
    #dataTotR=numpy.zeros(latticeShape)
    #Lcount=0
for R in Rs:

   	R=int(R)

   	# Load the data.
   	print("%s) Loading replicate %d"%(datetime.datetime.now(),R))
   	#Ls=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
   	Ls=list(f["/Simulations/%07d/Lattice"%(R)])
  	
	for L in Ls[0:finalTime+1]:
		L=int(L)
		#print("%s) Binning replicate %d, lattice %d"%(datetime.datetime.now(),R,L))
        	data=f["/Simulations/%07d/Lattice/%010d"%(R,L)].value
        	if data.shape[0] != latticeShape[0] or data.shape[1] != latticeShape[1] or data.shape[2] != latticeShape[2] or data.shape[3] != latticeShape[3]:
        		print("Lattice %d:%d had the wrong shape: %s"%(R,L,data.shape));
           		quit()
       
    		SubvolumeCount=sum((data==(species+1)).astype(int),3)
    		if sum(sum(sum(SubvolumeCount,2),1))>onThreshold:
    			l, m, n = SubvolumeCount.nonzero()
    			print("%s) Binning replicate %d, lattice %d"%(datetime.datetime.now(),R,L))
		#print(l)
		#print(m)
		#print(n)
   			if (len(l)==len(m)) & (len(m)==len(n)):
	   			for x in range(0,len(l)):
	   				count=SubvolumeCount[l[x],m[x],n[x]]
	   				counts[l[x],m[x],n[x],count]+=1
	   			
	   			Lcount +=1
		     
# Close the file.
f.close()

# Calculate and save the pdf.
#print("Lcount = %d"%(Lcount))
#counts[:,:,:,0]=len(Rs)*len(Ls)-sum(counts,3)
counts[:,:,:,0]=Lcount-sum(counts,3)
#totalCounts=sum(counts,3)
#pdf=zeros(latticeShape)
#pdf=zeros(countsShape)
#for x in range(0,countsShape[0]):
#    for y in range(0,countsShape[1]):
#        for z in range(0,countsShape[2]):
#            for p in range(0,countsShape[3]):
#                pdf[x,y,z,p]=float(counts[x,y,z,p])/totalCounts[x,y,z]

cellsave(outputDir,counts,indices);
print("Binned %d data points for lattice size %s to %s"%(sum(counts),counts.shape,outputDir))


