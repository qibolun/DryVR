from math import ceil
# Write data to file
def write_to_file(Sim_Result, write_path, type):
    # Write bloat file
    if type == 'simulation':
        with open(write_path, 'w') as write_file:
            for interval in Sim_Result:
                for item in interval:
                    write_file.write(str(item) + ' ')
                write_file.write('\n')




def read_from_file(read_path, type):
	if type == 'simulation':
		trace = []
		with open(read_path, 'r') as trace_file:
			for line in trace_file:
				# Extract data and append to trace
				data = [float(x) for x in line.split()]
				trace.append(data)    
	if type == 'reachtube_single':
		tube = []
		with open(read_path, 'r') as trace_file:
			next(trace_file)
			for line in trace_file:
				# Extract data and append to trace
				data = [float(x) for x in line.split()]
				tube.append(data)    
		return tube
	return trace          


def Reachtube_trunk_List(reachtube, time_interval):
	reachtube_length = len(reachtube)
	dimensions = len(reachtube[0])-1
	roundFactor = 2
	splitFactor = 10 #split all tubes into 10 pieces based on global time
	if reachtube[1][0] - reachtube[0][0] > time_interval[1]-time_interval[0]:
		print "The time step is larger than time interval, System is unknown and verification abort"
		exit()
	if reachtube_length %2 !=0:
		print "Reachtube length is not even, please check!"
		exit()
	initialSetList = []
	timeList = []

	find_flag = 0
	transSet = []
	for i in range(0, reachtube_length, 2):
		if (round(reachtube[i][0],roundFactor) >= time_interval[0]) & (round(reachtube[i+1][0],roundFactor) <= time_interval[1]):
			transSet.append(reachtube[i])
			transSet.append(reachtube[i+1])

	interval = (round(transSet[-1][-1],roundFactor) - round(transSet[0][-1],roundFactor))/splitFactor
	baseTime = round(transSet[0][-1],roundFactor)
	for i in range(splitFactor):
		timeLower = baseTime + i*interval
		timeUpper = baseTime + (i+1)*interval
		lowerbound = [float('inf')]*(dimensions-1)
		upperbound = [-float('inf')]*(dimensions-1)
		for j in range(0, len(transSet), 2):
			curLow = transSet[j]
			curHigh = transSet[j+1]
			if curLow[-1]>=timeLower and curHigh[-1]<=timeUpper:
				for k in range(1,dimensions):
					lowerbound[k-1] = min(lowerbound[k-1],curLow[k])
					upperbound[k-1] = max(upperbound[k-1],curHigh[k])
		initialSetList.append([lowerbound,upperbound])
		timeList.append([timeLower,timeUpper])





	#timeDelta = (time_interval[1]-time_interval[0])/2


	# timeList = []
	# #split the time_interval by smaller chunk (chunk_step each)
	# chunkNum = int(ceil(time_interval[1]-time_interval[0])/chunk_step)
	# print time_interval,chunkNum
	# timeLower = time_interval[0]
	# timeUpper = time_interval[0]+chunk_step

	# for _ in range(chunkNum):
	# 	find_flag = 0
	# 	lower_bound = []
	# 	upper_bound = []
	# 	for i in range(1,dimensions):
	# 		lower_bound.append('nan')
	# 		upper_bound.append('nan')
	# 	timeRange = []
	# 	for i in range(0, reachtube_length, 2):
	# 		#print reachtube[i][0],reachtube[i+1][0]
	# 		#print reachtube[i][0]>= timeLower, float(reachtube[i+1][0]) <= float(timeUpper)

	# 		if (round(reachtube[i][0],2) >= timeLower) and (round(reachtube[i+1][0],2) <= timeUpper):
	# 			timeRange.append(reachtube[i][-1])
	# 			timeRange.append(reachtube[i+1][-1])
	# 			if find_flag == 0:
	# 				for dim in range(1,dimensions):
	# 					lower_bound[dim-1] = reachtube[i][dim]
	# 					upper_bound[dim-1] = reachtube[i+1][dim]
	# 			else:
	# 				for dim in range(1,dimensions):
	# 					lower_bound[dim-1] = min(lower_bound[dim-1], reachtube[i][dim])
	# 					upper_bound[dim-1] = max(upper_bound[dim-1], reachtube[i+1][dim])
	# 	#this time range is caused by rounding error, just skip it
	# 	if len(timeRange)<2:
	# 		continue
	# 	#print timeRange,timeLower,timeUpper
	# 	timeLow = round(timeRange[0],2)
	# 	timeHigh = round(timeRange[-1],2)
	# 	initialSetList.append([lower_bound,upper_bound])
	# 	timeList.append([timeLow,timeHigh])
	# 	timeLower = time_interval[0]+(_+1)*chunk_step
	# 	timeUpper = time_interval[0]+(_+2)*chunk_step

	return initialSetList,timeList

	#split the time_interval into smaller chunck


def Reachtube_trunk(reachtube, time_interval):
	reachtube_length = len(reachtube)
	dimensions = len(reachtube[0])-1
	# print dimensions
	# print reachtube[0]
	if reachtube[1][0]-reachtube[0][0] > time_interval[1]-time_interval[0]:
		print "The time step is larger than time interval, System is unknown and verification abort"
		exit()

	if reachtube_length % 2 != 0:
		print('Reachtube length is not even, please check!')
		return None


	find_flag = 0
	lower_bound = []
	upper_bound = []
	for i in range(1,dimensions):
		lower_bound.append('nan')
		upper_bound.append('nan')
	timeRange = []
	for i in range(0, reachtube_length, 2):
		if (reachtube[i][0] >= time_interval[0]) & (reachtube[i][0] <= time_interval[1]):
			timeRange.append(reachtube[i][-1])
			timeRange.append(reachtube[i+1][-1])
			if find_flag == 0:
				find_flag = 1
				for dim in range(1,dimensions):
					lower_bound[dim-1] = reachtube[i][dim]
					upper_bound[dim-1] = reachtube[i+1][dim]
			else:
				for dim in range(1,dimensions):
					lower_bound[dim-1] = min(lower_bound[dim-1], reachtube[i][dim])
					upper_bound[dim-1] = max(upper_bound[dim-1], reachtube[i+1][dim])

	#timeDelta = (time_interval[1]-time_interval[0])/2

	if len(timeRange)<2:
		print("cannot find transition block, result unknown")
		exit()
	
	timeLow = timeRange[0]
	timeHigh = timeRange[-1]

	# double check output
	for dim in range(1,dimensions):
		if lower_bound[dim-1] > upper_bound[dim-1]:
			print('Find reach set in given time interval is wrong. The computed lower bound is greater than the upper bound!')
			return None
	# print lower_bound, "??????????????????"
	return lower_bound, upper_bound, timeLow, timeHigh