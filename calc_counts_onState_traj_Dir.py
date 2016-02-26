import datetime
import os
import sys
from os import listdir
from numpy import *
import h5py
from robertslab.cellio import *

if len(sys.argv) < 6:
    print "Usage: calc_rdme_pdf.py output_dir inputFile species onThreshold i [j k l m ...]"
    quit()

outputDir=sys.argv[1]
inputFile=sys.argv[2]
species=int(sys.argv[3])
onThreshold=int(sys.argv[4])
indices=()
for i in range(5,len(sys.argv)):
    indices+=(int(sys.argv[i]),)

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
    #Rs=[1]
print("Processing %d replicates"%(len(Rs)))
meanDensity=zeros((len(Rs),latticeShape[0],latticeShape[1],latticeShape[2]))
    # Go through each replicate.
    #dataTotR=numpy.zeros(latticeShape)
    #Lcount=0
counts=zeros((100,latticeShape[0],latticeShape[1],latticeShape[2],latticeShape[3]+1))
countsShape=counts.shape
print("Created empty array for counts: %s"%(counts.shape,))
#onEvent=0
#events=zeros((50,100))
Lcount=zeros((len(counts[:,0,0,0,0]),1))
###timesOn=[]
j=0

p=0
for R in Rs[:7]:

   	R=int(R)
   	# Load the data.
   	print("%s) Loading replicate %d"%(datetime.datetime.now(),R))
   	#Ls=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
   	Ls=list(f["/Simulations/%07d/Lattice"%(R)])
	#counts=zeros((20,latticeShape[0],latticeShape[1],latticeShape[2],latticeShape[3]+1))
	#countsShape=counts.shape
	#print("Created empty array for counts: %s"%(counts.shape,))
	#Lcount=0
	onEvent=0
	events=zeros((50,200))
	##Lcount=zeros((len(events[:,0]),1))	  	
	timesOn=[]
	#j=0
	for L in Ls:
		L=int(L)
		#print("%s) Binning replicate %d, lattice %d"%(datetime.datetime.now(),R,L))
        	data=f["/Simulations/%07d/Lattice/%010d"%(R,L)].value
        	if data.shape[0] != latticeShape[0] or data.shape[1] != latticeShape[1] or data.shape[2] != latticeShape[2] or data.shape[3] != latticeShape[3]:
        		print("Lattice %d:%d had the wrong shape: %s"%(R,L,data.shape));
           		quit()
       
    		SubvolumeCount=sum((data==(species+1)).astype(int),3)
    		if sum(sum(sum(SubvolumeCount,2),1))>onThreshold:
			timesOn.extend([L])
			
	
	
	for i in range(1,len(timesOn)):
		if timesOn[i]-timesOn[i-1]==1:
			j += 1
			events[onEvent,j]=timesOn[i]
		else:
			j=0
			onEvent +=1 
			events[onEvent,j]=timesOn[i]

	for k in range(onEvent):
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

cellsave(outputDir,counts,indices);
print("Binned %d data points for lattice size %s to %s"%(sum(counts),counts.shape,outputDir))


