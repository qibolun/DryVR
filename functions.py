from igraph import *
from InOutput import *
import random
from Global_Disc import *
from ExamplesPython.Car_Sim import TC_Simulate

#import matlab.engine
def buildGraph(vertex,edge,transtime,Time_horizon):
	g = Graph(directed = True)
	g.add_vertices(len(vertex))
	divid_intervals = [1 for _ in range(len(edge))]
	remainTime = [0 for _ in range(len(vertex))]
	g.add_edges(edge)

	#check if graph is dag
	assert g.is_dag()==True, "Graph provided is not a DAG, quit()"

	g.vs["label"] = vertex
	g.vs["name"] = vertex
	g.vs["remainTime"] = remainTime
	g.es["label"] = transtime
	g.es["trans_time"] = transtime
	g.es["divid"] = divid_intervals

	Compute_Order = g.topological_sorting(mode=OUT)
	for node in Compute_Order:
		if len(g.predecessors(node)) == 0: 	
			g.vs[node]["remainTime"]  = Time_horizon

	print 'graph', g.vs["remainTime"]


	PT_Pic = plot(g,"curgraph.png",margin=40)
	PT_Pic.save()
	return g

def refineGraph(g):
	label = g.es["label"]
	divid = g.es["divid"]

	maxidx = [(label[i][1]-label[i][0])/float(divid[i]) for i in range(len(label))]
	idx = maxidx.index(max(maxidx))
	divid[idx] +=1 
	g.es["divid"] = divid

def simulate(g,initialCondition,Time_horizon):
	retval = {}
	Compute_Order = g.topological_sorting(mode=OUT)
	Current_Vertex = Compute_Order[0]
	remainTime = Time_horizon
	Current_Time = 0


	dimensions = len(initialCondition)+1

	simResult = []

	while remainTime>0:
		print '-----------------------------------------------------'
		print 'Current State', g.vs[Current_Vertex]['label']

		Current_successors = g.successors(Current_Vertex)
		if len(Current_successors)==0:
			Transite_Time = remainTime
			print("Last mode, no more transitions, will stop at %f second" % (Transite_Time))
		else:
			Current_Successor = random.choice(Current_successors)
			edgeid = g.get_eid(Current_Vertex,Current_Successor)
			Current_transtime = g.es[edgeid]["label"]
			Transite_Time = float(random.uniform(Current_transtime[0],Current_transtime[1]))
			print("Will transite to mode %s at %f second" % (g.vs[Current_Successor]["label"], Transite_Time))

		curLabel = g.vs[Current_Vertex]['label']
		Current_Simulation = TC_Simulate(curLabel,initialCondition,Transite_Time)
		

		retval[g.vs[Current_Vertex]['name']] = retval.get(g.vs[Current_Vertex]['name'],[])
		for i in range (len(Current_Simulation)):
			retval[g.vs[Current_Vertex]['name']].append(Current_Simulation[i])
			Current_Simulation_row = [Current_Simulation[i][0] + Current_Time]
			for j in range (1,len(Current_Simulation[0])):
				Current_Simulation_row.append(Current_Simulation[i][j])
			simResult.append(Current_Simulation_row)

		#simResult+=Current_Simulation
		remainTime-=Transite_Time
		initialCondition = Current_Simulation[-1][1:]
		Current_Time = Current_Time + Transite_Time

		Current_Vertex = Current_Successor
	#print ("?")
	write_to_file(simResult,'output/Traj.txt','simulation')
	return retval


def Initial_Delta(Initial_Set):
	if len(Initial_Set[1])==len(Initial_Set[0]):
		delta = [(Initial_Set[1][dim] - Initial_Set[0][dim])/2 for dim in range (len(Initial_Set[1]))]
		return delta
	else:
		print('Initial set format irregular!')
		return None

def Center_Initial(Initial_Set):
	if len(Initial_Set[1])==len(Initial_Set[0]):
		Center_initial = [(Initial_Set[1][dim] + Initial_Set[0][dim])/2 for dim in range (len(Initial_Set[1]))]
		return Center_initial
	else:
		print('Initial set format irregular!')
		return None

def ReachTube(g,Initial_Set,Time_horizon):
	
	retval = {}

	Num_of_traces = 10

	#Remain_Time = Time_horizon

	# Initialize the initial set for all vertices
	num_of_vertices = g.vcount()
	Init_Values = []
	time_Concat = []
	for i in range(num_of_vertices):
		Init_Values.append([])
		time_Concat.append([])

	Init_Values[0].append(Initial_Set)
	#Time use to concat
	time_Concat[0].append((0,0))


	Compute_Order = g.topological_sorting(mode=OUT)
	print 'order',Compute_Order
	vertex_order = 0
	#g.vs[Compute_Order[vertex_order]]["remainTime"] = Time_horizon
	Remain_Time = Time_horizon
	breakflag = False
	modeSwitchDic = {}
	reachfile = []
	while Remain_Time > 0:
		print("-----------------------------------------------------------------")
		Current_Vertex = Compute_Order[vertex_order]
		print("Current State is the %d th mode with name %s" % (Current_Vertex, g.vs[Current_Vertex]["name"]))
		Current_successors = g.successors(Current_Vertex)
		Current_predeceesors = g.predecessors(Current_Vertex)

		for s in Current_successors:
			modeSwitchDic[s] = str(Current_Vertex) + '->' + str(s)
		if len(Current_predeceesors) == 0:
			modeSwitchDic[Current_Vertex] = str(Current_Vertex)
			
		if len(Current_successors)==0:
			transite_time_max = float(Remain_Time)
			print("Last mode, no more transitions, will stop at %f seconds" % (transite_time_max))
			if vertex_order == len(Compute_Order)-1:
				breakflag = True
		else:
			# transite_time_max is the maximum time to stay in the current mode, and so is transite_time_min
			transite_times_max = []
			transite_times_min = []

			for j in range(len(Current_successors)):
				Current_Successor = Current_successors[j]
				edgeid = g.get_eid(Current_Vertex,Current_Successor)
				Current_transtime = g.es[edgeid]["trans_time"]
				g.vs[Current_Successor]["remainTime"] = max(g.vs[Current_Successor]["remainTime"],g.vs[Current_Vertex]["remainTime"]-Current_transtime[0])
				transite_times_min.append(Current_transtime[0])
				transite_times_max.append(Current_transtime[1])

			transite_time_min = min(transite_times_min)
			transite_time_max = max(transite_times_max)
			transite_time_max = float(min(transite_time_max,Remain_Time))

		reachfile.append('% '+g.vs[Current_Vertex]['name']+' '+modeSwitchDic[Current_Vertex]+'\n')

		if len(Init_Values[Current_Vertex][0]) == 0:
			print("Vertex order dismatch! The initial value for current vertex is unknown!")
		else:
			append_flag = 0
			for cnt in range(len(Init_Values[Current_Vertex])):
				Current_Delta = Initial_Delta(Init_Values[Current_Vertex][cnt])
				print("Initial Condition is ", Init_Values[Current_Vertex][cnt])
				print("Initial Delta is", Current_Delta)
				print("Time used to concat is", time_Concat[Current_Vertex][cnt])

				Initial_lower_bound = Init_Values[Current_Vertex][cnt][0]
				Initial_upper_bound = Init_Values[Current_Vertex][cnt][1]
				Center_trace_initial = Center_Initial(Init_Values[Current_Vertex][cnt])

				curLabel = g.vs[Current_Vertex]['label']
			
				traces = []
				traces.append(TC_Simulate(curLabel,Center_trace_initial,transite_time_max))
				for _ in range(Num_of_traces):
					newInit = [random.uniform(Initial_lower_bound[ii],Initial_upper_bound[ii]) for ii in range(len(Initial_lower_bound))]
					traces.append(TC_Simulate(curLabel,newInit,transite_time_max))


				k,gamma = Global_Discrepancy(curLabel,Current_Delta, 0, 2,traces)

				retval[g.vs[Current_Vertex]['name']] = retval.get(g.vs[Current_Vertex]['name'],[])
				if append_flag == 0:
					Current_reachtube = Bloat_to_tube(curLabel, k, gamma, Current_Delta, 'output/Reachtube' + g.vs[Current_Vertex]['name'] + str(Current_Vertex) + '.txt', 'new',time_Concat[Current_Vertex][cnt],traces)
					retval[g.vs[Current_Vertex]['name']] += Current_reachtube
					append_flag = 1
				else:
					Current_reachtube = Bloat_to_tube(curLabel, k, gamma, Current_Delta, 'output/Reachtube' + g.vs[Current_Vertex]['name'] + str(Current_Vertex) + '.txt', 'append',time_Concat[Current_Vertex][cnt],traces)
					retval[g.vs[Current_Vertex]['name']] += Current_reachtube

				for t in Current_reachtube:
					curline = ''
					for val in t:
						curline +=str(val)+' '
					curline += '\n'
					reachfile.append(curline)
				# print("Finish Simulating for Mode %s" % (g.vs[Current_Vertex]['name']))

				print("The discrepancy function for current mode is",k,gamma)

				if len(Current_successors)!=0:
					for j in range(len(Current_successors)):
						Current_Successor = Current_successors[j]
						edgeid = g.get_eid(Current_Vertex,Current_Successor)
						

						## Start of modification
						Current_transtime = g.es[edgeid]["trans_time"]
						# Change to float numbers 
						Current_transtime = (float(Current_transtime[0]),float(Current_transtime[1]))
						Intervals_divided = g.es[edgeid]["divid"]



						for cnt_intval in range (Intervals_divided):
							print 'Interval_divided', Intervals_divided
							Time_range = Current_transtime[1] - Current_transtime[0]
							Current_time_interval = [Current_transtime[0] + (cnt_intval)*(Time_range/Intervals_divided), Current_transtime[0] + (cnt_intval+1)*(Time_range/Intervals_divided)]
							Trans_initial_lower, Trans_initial_upper,timeLow,timeHigh= Reachtube_trunk(Current_reachtube, Current_time_interval)
							Init_Values[Current_Successor].append([Trans_initial_lower, Trans_initial_upper])
							time_Concat[Current_Successor].append((timeLow,timeHigh))

							
		vertex_order += 1
		if not breakflag:
			Remain_Time	= g.vs[Compute_Order[vertex_order]]["remainTime"]
		else:
			Remain_Time = 0
		# print 'name is ', g.vs['name']
		# print 'remainTime is ',g.vs["remainTime"]
	
	return retval,reachfile


def ReachTubeSP(g,Initial_Set,Time_horizon):
	retval = {}
	Num_of_traces = 10
	#Remain_Time = Time_horizon
	# Initialize the initial set for all vertices
	num_of_vertices = g.vcount()
	Init_Values = []
	time_Concat = []
	Init_LargeSet = []
	for i in range(num_of_vertices):
		Init_Values.append([])
		time_Concat.append([])
		Init_LargeSet.append([])
	Init_Values[0].append([Initial_Set])
	Init_LargeSet[0].append(Initial_Set)
	#Time use to concat
	time_Concat[0].append([(0,0)])


	Compute_Order = g.topological_sorting(mode=OUT)
	vertex_order = 0
	#g.vs[Compute_Order[vertex_order]]["remainTime"] = Time_horizon
	Remain_Time = Time_horizon
	breakflag = False
	modeSwitchDic = {}
	f = open('output/reachTube.txt','w')
	while Remain_Time > 0:
		print("-----------------------------------------------------------------")
		Current_Vertex = Compute_Order[vertex_order]
		print("Current State is the %d th mode with name %s" % (Current_Vertex, g.vs[Current_Vertex]["name"]))
		Current_successors = g.successors(Current_Vertex)
		Current_predeceesors = g.predecessors(Current_Vertex)

		for s in Current_successors:
			modeSwitchDic[s] = str(Current_Vertex) + '->' + str(s)
		if len(Current_predeceesors) == 0:
			modeSwitchDic[Current_Vertex] = str(Current_Vertex)
		if len(Current_successors)==0:
			transite_time_max = float(Remain_Time)
			print("Last mode, no more transitions, will stop at %f seconds" % (transite_time_max))
			if vertex_order == len(Compute_Order)-1:
				breakflag = True
		else:
			# transite_time_max is the maximum time to stay in the current mode, and so is transite_time_min
			transite_times_max = []
			transite_times_min = []

			for j in range(len(Current_successors)):
				Current_Successor = Current_successors[j]
				edgeid = g.get_eid(Current_Vertex,Current_Successor)
				Current_transtime = g.es[edgeid]["trans_time"]
				g.vs[Current_Successor]["remainTime"] = max(g.vs[Current_Successor]["remainTime"],g.vs[Current_Vertex]["remainTime"]-Current_transtime[0])
				transite_times_min.append(Current_transtime[0])
				transite_times_max.append(Current_transtime[1])

			transite_time_min = min(transite_times_min)
			transite_time_max = max(transite_times_max)
			transite_time_max = float(min(transite_time_max,Remain_Time))

		f.write('% '+g.vs[Current_Vertex]['name']+' '+modeSwitchDic[Current_Vertex]+'\n')

		if len(Init_Values[Current_Vertex][0][0]) == 0:
			print("Vertex order dismatch! The initial value for current vertex is unknown!")
		else:
			append_flag = 0
			for cnt in range(len(Init_Values[Current_Vertex])):
				retval[g.vs[Current_Vertex]['name']] = retval.get(g.vs[Current_Vertex]['name'],[])
				tubeHolder = []

				newF = open('output/ReachTube'+str(Current_Vertex)+'.txt','w')
				curLabel = g.vs[Current_Vertex]['label']

				#calculate k and gamma for large set
				traces = []
				Initial_lower_bound = Init_LargeSet[Current_Vertex][cnt][0]
				Initial_upper_bound = Init_LargeSet[Current_Vertex][cnt][1]
				Center_trace_initial = Center_Initial(Init_LargeSet[Current_Vertex][cnt])
				Current_Delta = Initial_Delta(Init_LargeSet[Current_Vertex][cnt])
				traces.append(TC_Simulate(curLabel, Center_trace_initial, transite_time_max))
				for _ in range(Num_of_traces):
					newInit = [random.uniform(Initial_lower_bound[ii],Initial_upper_bound[ii]) for ii in range(len(Initial_lower_bound))]
					traces.append(TC_Simulate(curLabel,newInit,transite_time_max))
				k,gamma = Global_Discrepancy(curLabel,Current_Delta, 0, 2, traces)
				print("The discrepancy function for current mode is",k,gamma)

				for rs in range(len(Init_Values[Current_Vertex][cnt])):
					Current_Delta = Initial_Delta(Init_Values[Current_Vertex][cnt][rs])
					#print("Initial Condition is ", Init_Values[Current_Vertex][cnt][rs])
					
					#print("Time used to concat is", time_Concat[Current_Vertex][cnt])

					Center_trace_initial = Center_Initial(Init_Values[Current_Vertex][cnt][rs])

					traces = []
					traces.append(TC_Simulate(curLabel, Center_trace_initial, transite_time_max))

					Current_reachtube = Bloat_to_tubeNoIO(curLabel, k, gamma, Current_Delta, time_Concat[Current_Vertex][cnt][rs],traces)
					tubeHolder.append(Current_reachtube)
					newF.write('===========================================')
					for t in Current_reachtube:
						for val in t:
							newF.write(str(val)+ ' ')
						newF.write('\n')
				newF.close()

				resultTube = concatTube(tubeHolder)
				if cnt == 0:
					writeTraceToFile(curLabel,resultTube,'output/Reachtube'+g.vs[Current_Vertex]['name']+str(Current_Vertex)+'.txt', 'new')
				else:
					writeTraceToFile(curLabel,resultTube,'output/Reachtube'+g.vs[Current_Vertex]['name']+str(Current_Vertex)+'.txt', 'append')

				retval[g.vs[Current_Vertex]['name']] += resultTube
				#write this into a reachtube output file
				for t in resultTube:
					for val in t:
						f.write(str(val)+' ')
					f.write('\n')

				
				if len(Current_successors)!=0:
					for j in range(len(Current_successors)):
						Current_Successor = Current_successors[j]
						edgeid = g.get_eid(Current_Vertex,Current_Successor)
						

						## Start of modification
						Current_transtime = g.es[edgeid]["trans_time"]
						# Change to float numbers 
						Current_transtime = (float(Current_transtime[0]),float(Current_transtime[1]))
						Intervals_divided = g.es[edgeid]["divid"]

						#there is no interval divided anymore
						
						initialSetList,timeList = Reachtube_trunk_List(resultTube, Current_transtime)
						Trans_initial_lower, Trans_initial_upper,timeLow,timeHigh = Reachtube_trunk(resultTube, Current_transtime)
						Init_Values[Current_Successor].append(initialSetList)
						time_Concat[Current_Successor].append(timeList)
						Init_LargeSet[Current_Successor].append([Trans_initial_lower, Trans_initial_upper])

						#print 'HHHHHHHH',Init_Values[Current_Successor]
						print 'AAAAAAAA',time_Concat[Current_Successor]
						print 'CCCCCCCC',Init_LargeSet[Current_Successor]


						# for cnt_intval in range (Intervals_divided):
						# 	print 'Interval_divided', Intervals_divided
						# 	Time_range = Current_transtime[1] - Current_transtime[0]
						# 	Current_time_interval = [Current_transtime[0] + (cnt_intval)*(Time_range/Intervals_divided), Current_transtime[0] + (cnt_intval+1)*(Time_range/Intervals_divided)]
						# 	Trans_initial_lower, Trans_initial_upper,timeLow,timeHigh= Reachtube_trunk(Current_reachtube, Current_time_interval)
						# 	Init_Values[Current_Successor].append([Trans_initial_lower, Trans_initial_upper])
						# 	time_Concat[Current_Successor].append((timeLow,timeHigh))

							
		vertex_order += 1
		if not breakflag:
			Remain_Time	= g.vs[Compute_Order[vertex_order]]["remainTime"]
		else:
			Remain_Time = 0
		# print 'name is ', g.vs['name']
		# print 'remainTime is ',g.vs["remainTime"]
	f.close()
	return retval		


def concatTube(tubes):
	#return the tube if there is only one tube in the dictionary
	if len(tubes) == 1:
		return tubes[0]

	tubeDic = {}
	for tube in tubes:
		for i in range(0,len(tube),2):
			lowerBound = tube[i]
			upperBound = tube[i+1]
			key = round(lowerBound[-1],2)
			#I assue that time start with same lower bound will have same upper bound
			if not key in tubeDic:
				tubeDic[key] = [lowerBound,upperBound]
			else:
				#skip the first inmode time dimension and last global time dimension
				for j in range(1,len(lowerBound)-1):
					tubeDic[key][0][j] = min(tubeDic[key][0][j],lowerBound[j])
					tubeDic[key][1][j] = max(tubeDic[key][1][j],upperBound[j])

	#Now I just assume all tubes are merged in one
	retval = []
	for key in sorted(tubeDic):
		#print key
		retval.append(tubeDic[key][0])
		retval.append(tubeDic[key][1])
	return retval



