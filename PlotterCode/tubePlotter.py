import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys

file = open('reachTube.txt','r')
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
	
		x1rect = patches.Rectangle((lb[-1],lb[1]),ub[-1]-lb[-1],ub[1]-lb[1],color=colors[counter%5],alpha=0.7)
		#x2rect = patches.Rectangle((lb[-1],lb[5]),ub[-1]-lb[-1],ub[5]-lb[5],color='green',alpha=0.7)
	
		#y1rect = patches.Rectangle((lb[0],abs(lb[2])),ub[0]-lb[0],ub[2]-lb[2],color='red',alpha=0.7)
		#y2rect = patches.Rectangle((lb[0],abs(lb[6])),ub[0]-lb[0],ub[6]-lb[6],color='green',alpha=0.7)
		#print x1rect
		axarr.add_patch(x1rect)
		#axarr.add_patch(x2rect)
		#axarr.add_patch(y1rect)
		#axarr.add_patch(y2rect)
	counter+=1
axarr.plot()
plt.show()
f.savefig('reachTube.eps', format='eps', dpi=1200)
	#plot x and y for car1


