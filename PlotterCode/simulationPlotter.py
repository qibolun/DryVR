import matplotlib.pyplot as plt
import matplotlib.patches as patches
from InOutput import *
import sys


#Current_simulation = read_from_file('output/unsafeSim', 'simulation')
fi = open('output/unsafeSim')
dic = {}
curMode = None
for line in fi:
	line = line.strip().split(',')
	if len(line) == 1:
		curMode = line[0]
		dic[curMode] = dic.get(curMode,[])
	else:
		dic[curMode].append([float(i) for i in line])

dim = len(dic)
f, axarr = plt.subplots(2,dim, sharex='col', sharey = 'row')
title = ['speedup','ch_left','speedup','brake','ch_right','cruise']

order = ["Acc1;Const","TurnLeft;Const","Acc2;Const","Dec;Const","TurnRight;Const","Const;Const"]
for idx,curmode in enumerate(order):
	Current_simulation = dic[curmode]
	t = [cur[0] for cur in Current_simulation]
	x1 = [cur[1] for cur in Current_simulation]
	x2 = [cur[5] for cur in Current_simulation]
	y1 = [abs(cur[2]) for cur in Current_simulation]
	y2= [abs(cur[6]) for cur in Current_simulation]
	axarr[0][idx].set_title(title[idx],fontsize=12)
	axarr[0][idx].plot(t,x1,color='red')
	axarr[0][idx].plot(t,x2,color='green')
	axarr[1][idx].plot(t,y1,color='red')
	axarr[1][idx].plot(t,y2,color='green')

yuplim = axarr[0][4].get_ylim()
ylolim = axarr[1][4].get_ylim()
axarr[0][4].set_ylim(yuplim)
axarr[1][4].set_ylim(ylolim)
uprect = patches.Rectangle((7,yuplim[0]),3,yuplim[1]-yuplim[0],edgecolor='None',facecolor='grey',alpha=0.5)
lowrect = patches.Rectangle((7,ylolim[0]),3,ylolim[1]-ylolim[0],edgecolor='None',facecolor='grey',alpha=0.5)
axarr[0][4].add_patch(uprect)
axarr[1][4].add_patch(lowrect)

axarr[0][4].plot()
axarr[1][4].plot()
plt.show()
f.savefig('simulation.eps', format='eps', dpi=1200)
	#plot x and y for car1


