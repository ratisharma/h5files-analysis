import datetime
import os
import sys
from os import listdir
from numpy import *
import h5py
from cellio import *

if len(sys.argv) < 6:
    print "Usage: calc_rdme_pdf.py output_dir inputFile species onThreshold i [j k l m ...]"
    quit()

outputDir=sys.argv[1]
print outputDir
inputFile=sys.argv[2]
species=int(sys.argv[3])
onThreshold=int(sys.argv[4])
#filenum=int(sys.argv[5])
indices=()
print(len(sys.argv))
for i in range(5,len(sys.argv)):
    print sys.argv[i]
    indices+=(int(sys.argv[i]),)
    #indices

# Create the arrays to store the stats.
Xtot=arange(0,1)
Ctot=zeros(1,dtype=int32)

# Create an array for the counts.
lattice=zeros((50,50,50,16))
latticeShape=lattice.shape
f=h5py.File(inputFile, 'r')    
print("Processing %s file"%(inputFile))

# Get the list of replicates.
Rs=list(f["/Simulations"])
#Rs=[1,2,3]
print("Processing %d replicates"%(len(Rs)))

# Go through each replicate.
    
j=0
p=0
events=zeros((20*len(Rs),500))

onEvent=0
for R in Rs:
    R=int(R)
    # Load the data.
    print("%s) Loading replicate %d"%(datetime.datetime.now(),R))
    #Ls=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    Ls=list(f["/Simulations/%07d/Lattice"%(R)])
    timesOn=[]  	
    for L in Ls:
	L=int(L)
	#print("%s) Binning replicate %d, lattice %d"%(datetime.datetime.now(),R,L))
       	data=f["/Simulations/%07d/Lattice/%010d"%(R,L)].value
       	if data.shape[0] != latticeShape[0] or data.shape[1] != latticeShape[1] or data.shape[2] != latticeShape[2] or data.shape[3] != latticeShape[3]:
       		print("Lattice %d:%d had the wrong shape: %s"%(R,L,data.shape));
       		quit()
       
	SubvolumeCount=sum((data==(species+1)).astype(int),3)
	if sum(sum(sum(SubvolumeCount,2),1))>=onThreshold:
		timesOn.append(L)
    #print timesOn			
	
    events[onEvent,0]=timesOn[0];	
    for i in range(1,len(timesOn)):
	if timesOn[i]-timesOn[i-1]==1:
		j += 1
		events[onEvent,j]=timesOn[i]
	else:
		j=0
		onEvent +=1 
		events[onEvent,j]=timesOn[i]
    onEvent+=1
    j=0
    #print("onEvent="),
    #print onEvent
    #print("events="),
    #print events
	     
# Close the file.
f.close()
cellsave(outputDir,events,indices);

