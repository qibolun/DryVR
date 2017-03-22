import matplotlib.pyplot as plt
import matplotlib.patches as patches
from functions import *
from InOutput import *
import sys



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
path = f.readline().strip().split(':')[1]

g = buildGraph(vertex,edge,transtime,timeHorizon)

num_ver = g.vcount()
title = ['speedup','ch_left','speedup','brake','ch_right','cruise']
f, axarr = plt.subplots(2,num_ver, sharex='col', sharey = 'row')
Compute_Order = g.topological_sorting(mode=OUT)
for idx,vertex in enumerate(Compute_Order):
	Current_reachtube = read_from_file('output/Reachtube'+g.vs[vertex]['name'] + str(vertex) +'.txt', 'reachtube_single')
	#print Current_reachtube
	lowerbound = [Current_reachtube[i] for i in range(0,len(Current_reachtube),2)]
	upperbound = [Current_reachtube[i+1] for i in range(0,len(Current_reachtube),2)]

	for i in range(len(lowerbound)):
		lb = lowerbound[i]
		ub = upperbound[i]
		#print lowerbound
		#print upperbound
		#print lb,ub
		x1rect = patches.Rectangle((lb[0],lb[1]),ub[0]-lb[0],ub[1]-lb[1],color='red',alpha=0.7)
		x2rect = patches.Rectangle((lb[0],lb[5]),ub[0]-lb[0],ub[5]-lb[5],color='green',alpha=0.7)
		#print (lb[0],lb[2]),ub[0]-lb[0],ub[2]-lb[1]
		#print yrect
		y1rect = patches.Rectangle((lb[0],abs(lb[2])),ub[0]-lb[0],ub[2]-lb[2],color='red',alpha=0.7)
		y2rect = patches.Rectangle((lb[0],abs(lb[6])),ub[0]-lb[0],ub[6]-lb[6],color='green',alpha=0.7)
		#print x1rect
		axarr[0,idx].add_patch(x1rect)
		axarr[0,idx].add_patch(x2rect)
		axarr[1][idx].add_patch(y1rect)
		axarr[1][idx].add_patch(y2rect)
	axarr[0][idx].set_title(title[idx],fontsize=12)
	axarr[0][idx].plot()
	axarr[1][idx].plot()
plt.show()
f.savefig('reachTube.eps', format='eps', dpi=1200)
	#plot x and y for car1


