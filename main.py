import sys
from functions import *
from classes import *
import random
import time
# import matlab.engine

filename = sys.argv[-1]
#check if the there is input file
assert len(sys.argv) == 2, "input file not provided"

f = open(filename)
vertex = eval(f.readline().strip().split(':')[1])
edge = eval(f.readline().strip().split(':')[1])
transtime = eval(f.readline().strip().split(':')[1])
initialSet = eval(f.readline().strip().split(':')[1])
unsafeSet = ':'.join(f.readline().strip().split(':')[1:])
timeHorizon = float(f.readline().strip().split(':')[1])


g = buildGraph(vertex,edge,transtime,timeHorizon)


#tunning parameter
randomNum = 0

initialSetLow = initialSet[0]
initialSetHigh = initialSet[1]

dimension = len(initialSetLow)
checker = uniformChecker(dimension,unsafeSet)


# eng = matlab.engine.start_matlab()
# eng.addpath(path,nargout=0)
# eng.setup(nargout=0)

start1 = time.time()
refineCounter = 0
refineTime = 0

#random Checking for point from initialSet
for i in range (randomNum):
	randomInit = []
	for j in range(dimension):
		randomInit.append(random.uniform(initialSetLow[j] ,initialSetHigh[j]))
	
	print 'Random Checking round', i, 'at point ', randomInit
	tube = simulate(g,randomInit,timeHorizon)
	for key in tube:
		safety = checker.checkSimuTube(tube[key],key)
		if safety == -1:
			end1 = time.time()
			print ("Simulation safety check is %f" % (float(end1) - float(start1)))
			print ("System Unsafe from simulation, halt verification")
			f = open('output/unsafeSim','w')
			for key in tube:
				f.write(key+'\n')
				for t in tube[key]:
					f.write(str(t)[1:-1])
					f.write('\n')
			f.close()

			exit()

end1 = time.time()
#start Checking for the system
stack = [InitialSet(initialSetLow,initialSetHigh)]
start2 = time.time()

print "-------------------------------------------------------------------"
print "verification begin"

while stack:
	curInit = stack.pop()
	print ("------cur init set-------")
	curInit.printSet()
	tubeDic = ReachTubeSP(g,[curInit.lowerbound,curInit.upperbound],timeHorizon)
	safe = 1
	exit()
	for key in tubeDic:
		curTube = tubeDic[key]
		safety = checker.checkReachTube(curTube,key)
		if safety == -1:
			print ("System Unsafe from reachtue computation, halt verification")
			end2 = time.time()
			print ("System has been refined for %d Times" % refineTime)
			print ("Simulation safety check is %f" % (float(end1) - float(start1)))
			print ("Verification safety check is %f" % (float(end2) - float(start2)))
			exit()

		elif safety == 0:
			print "System is unknown at ", key, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
			safe = 0



	if safe == 0:
		print ('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!REFINE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
		refineTime += 1
		if refineCounter == 5:
			refineGraph(g)
			print "***********************************refine graph*******************************************"
			print g.es["divid"]
			refineCounter = 0
			stack.append(curInit)
		else:
			if max(curInit.delta) == 0:
				print("thickness 0, refine graph")
				refineGraph(g)
				print g.es["divid"]
				stack.append(curInit)
			else:
				initOne,initTwo = curInit.split()
				stack.append(initOne)
				stack.append(initTwo)
			refineCounter+=1


end2 = time.time()

print ("System is Safe!")
print ("System has been refined for %d Times" % refineTime)
print ("Simulation safety check is %f" % (float(end1) - float(start1)))
print ("Verification safety check is %f" % (float(end2) - float(start2)))


