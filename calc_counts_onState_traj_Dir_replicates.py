
import datetime
import os
import sys
from os import listdir
from numpy import *
import h5py
from cellio import *

if len(sys.argv) < 7:
    print "Usage: calc_rdme_pdf.py output_dir inputFile species onThreshold replicate i [j k l m ...]"
    quit()

outputDir=sys.argv[1]
print outputDir
inputFile=sys.argv[2]
species=int(sys.argv[3])
onThreshold=int(sys.argv[4])
replicate=int(sys.argv[5])
indices=()
print(len(sys.argv))
for i in range(6,len(sys.argv)):
    print sys.argv[i]
    indices+=(int(sys.argv[i]),)
    #indices

print outputDir
print inputFile
print("species= "+ str(species))
print('onThreshold = '+ str(onThreshold))
print('replicate = ' + str(replicate))
# Create the arrays to store the stats.
Xtot=arange(0,1)
Ctot=zeros(1,dtype=int32)

# Create an array for the counts.
lattice=zeros((50,50,50,16))
latticeShape=lattice.shape
f=h5py.File(inputFile, 'r')    
print("Processing %s file"%(inputFile))

# Get the list of replicates.
j=0

p=0
R=int(replicate)
   	# Load the data.
print("%s) Loading replicate %d"%(datetime.datetime.now(),R))
Ls=list(f["/Simulations/%07d/Lattice"%(R)])
counts=zeros((35,latticeShape[0],latticeShape[1],latticeShape[2],latticeShape[3]+1))
countsShape=counts.shape
print("Created empty array for counts: %s"%(counts.shape,))
Lcount=0
onEvent=0
events=zeros((35,502))
Lcount=zeros((len(events[:,0]),1))	  	
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
print timesOn			
	
events[onEvent,0]=timesOn[0];	
for i in range(1,len(timesOn)):
	if timesOn[i]-timesOn[i-1]==1:
		j += 1
		events[onEvent,j]=timesOn[i]
	else:
		j=0
		onEvent +=1 
		events[onEvent,j]=timesOn[i]
print onEvent
print events

for k in range(onEvent+1):
	j=0
	Lcount[p]=0
	while events[k,j]>0:
	    data=f["/Simulations/%07d/Lattice/%010d"%(R,events[k,j])].value
	    SubvolumeCount=sum((data==(species+1)).astype(int),3)
	    l, m, n = SubvolumeCount.nonzero()
	    print("%s) Binning replicate %d, lattice %d"%(datetime.datetime.now(),R,events[k,j]))
	#print(l)
	#print(m)
	#print(n)
	    if (len(l)==len(m)) & (len(m)==len(n)):
		for x in range(0,len(l)):
			count=SubvolumeCount[l[x],m[x],n[x]]
			counts[p,l[x],m[x],n[x],count]+=1
	 		
		Lcount[p] +=1
	    j += 1
	counts[p,:,:,:,0]=Lcount[p]-sum(counts[p,:,:,:,:],3)
	print("p="+str(p))
	p+=1
		
	#totalCounts=sum(counts,3)
	#pdf=zeros(countsShape)
	#density=zeros(countsShape)
	#for x in range(0,countsShape[0]):
	#    for y in range(0,countsShape[1]):
	#        for z in range(0,countsShape[2]):
	#            for p in range(0,countsShape[3]):
 #		        pdf[x,y,z,p]=float(counts[x,y,z,p])/totalCounts[x,y,z]
	#		density[x,y,z,p]=p*pdf[x,y,z,p]
	#meanDensity[R,:,:,:]=sum(density,3)

	     
# Close the file.
f.close()
cellsave(outputDir,counts,indices);

print("Binned %d data points for lattice size %s to %s"%(sum(counts),counts.shape,outputDir))	
# Calculate and save the pdf.
#print("Lcount = %d"%(Lcount))
#counts[:,:,:,0]=len(Rs)*len(Ls)-sum(counts,3)
#counts[:,:,:,0]=Lcount-sum(counts,3)
#totalCounts=sum(counts,3)
#pdf=zeros(latticeShape)
#pdf=zeros(countsShape)
#for x in range(0,countsShape[0]):
#    for y in range(0,countsShape[1]):
#        for z in range(0,countsShape[2]):
#            for p in range(0,countsShape[3]):
#                pdf[x,y,z,p]=float(counts[x,y,z,p])/totalCounts[x,y,z]

#cellsave(outputDir,meanDensity,indices);
#print("Binned %d data points for lattice size %s to %s"%(sum(meanDensity),meanDensity.shape,outputDir))

#cellsave(outputDir,counts,indices);
#print("Binned %d data points for lattice size %s to %s"%(sum(counts),counts.shape,outputDir))


