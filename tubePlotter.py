import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys

file = open('output/reachTube.txt','r')


assert len(sys.argv) == 2, "Error, No dimension specified, Usage: python tubePlotter.py varNum"
dim = int(sys.argv[-1])
totalDim = 0
curMode = ''
tubeDic = {}
for line in file:
	line = line.strip().split()
	if line[0] == '%':
		curMode = line[1]
		if not curMode in tubeDic: 
			tubeDic[curMode] = []
	else:
		tubeDic[curMode].append([float(val) for val in line])
		totalDim = len(tubeDic[curMode][0])

if dim>= totalDim:
	print "Invalid dimension number, plotter halt"
	exit()



f, axarr = plt.subplots()
colors = ['red','yellow','green','blue','gray']
counter = 0
for key in tubeDic:
	Current_reachtube = tubeDic[key]
	#print Current_reachtube
	lowerbound = [Current_reachtube[i] for i in range(0,len(Current_reachtube),2)]
	upperbound = [Current_reachtube[i+1] for i in range(0,len(Current_reachtube),2)]

	for i in range(len(lowerbound)):
		lb = lowerbound[i]
		ub = upperbound[i]
	
		x1rect = patches.Rectangle((lb[-1],lb[dim]),ub[-1]-lb[-1],ub[dim]-lb[dim],color=colors[counter%5],alpha=0.7)
		axarr.add_patch(x1rect)
		
	counter+=1
axarr.plot()
plt.show()
f.savefig('reachTube.eps', format='eps', dpi=1200)
	#plot x and y for car1


