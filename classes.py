from z3 import *
import random

class InitialSet():
	def __init__(self, _lower, _upper):
		#print "construct",_upper,_lower
		self.upperbound = _upper
		self.lowerbound = _lower
		self.delta = [(_upper[i]-_lower[i])/2 for i in range(len(_upper))]
		self.reachTube = []
	
	def reachtube(self, _timeHorizon):
		pass

	def split(self):

		_index = self.delta.index(max(self.delta))
		TubeOneUpper = list(self.upperbound)
		TubeOneLower = list(self.lowerbound)
		TubeOneLower[_index]+=self.delta[_index]

		TubeTwoUpper = list(self.upperbound)
		TubeTwoUpper[_index]-=self.delta[_index]
		TubeTwoLower = list(self.lowerbound)

		#print '!',TubeOneLower
		return (InitialSet(TubeOneLower,TubeOneUpper), InitialSet(TubeTwoLower,TubeTwoUpper))

	def printSet(self):
		print ("--------------------------------")
		print (self.upperbound)
		print (self.lowerbound)
		print (self.delta)

#This is the Checker class to check the safety
# class Checker():
# 	def __init__(self,_dimension,_unsafe):
# 		self.vardic = {}
# 		self.unsafe = _unsafe

# 		for i in range(_dimension):
# 			self.vardic['v'+str(i+1)] = Real('v'+str(i+1))

# 		for key in self.vardic:
# 			self.unsafe = self.unsafe.replace(key,'self.vardic["'+key+'"]')


# 		#This construct the intersection solver
# 		unsafeset = self.unsafe.split('&&')
# 		constrains = []
# 		for i in range(len(unsafeset)):
# 			constrains.append(eval(unsafeset[i]))
# 		self.intersectionSolver = Solver()
# 		for con in constrains:
# 			self.intersectionSolver.add(con)
# 		print self.intersectionSolver
# 		#this construct the reverse of intersection solver
# 		safeset = self.unsafe.replace('<','ge').replace('>','le').replace('<=','gg').replace('>=','ll')
# 		safeset = safeset.replace('ge','>=').replace('le','<=').replace('gg','>').replace('ll','<')
# 		safeset = safeset.split('&&')
# 		# safeConstrains = []
# 		# for i in range(len(safeset)):
# 		# 	safeConstrains.append(eval(safeset[i]))
# 		self.containmentSolver = Solver()
# 		conStr = "Or("
# 		for s in safeset:
# 			conStr += s
# 			conStr += ','
# 		conStr = conStr[:-1] + ')'
# 		conStr = eval(conStr)
# 		self.containmentSolver.add(conStr)
# 		print self.containmentSolver


# 	def checkReachTube(self,tube):
# 		safe = 1
# 		for i in range(0,len(tube),2):
# 			lower = tube[i]
# 			upper = tube[i+1]
# 			if self._checkIntersection(lower,upper):
# 				print "System Intersect at", lower,upper
# 				if self._checkContainment(lower,upper):
# 					print lower
# 					print upper
# 					return -1
# 				else:
# 					safe = 0
# 		return safe

# 	def _checkContainment(self,lo,up):
# 		lolist = []
# 		uplist = []
# 		for i in range(1,len(lo)):
# 			lolist.append(self.vardic['v'+str(i)]>=lo[i])
# 			uplist.append(self.vardic['v'+str(i)]<=up[i])
# 		self.containmentSolver.push()
# 		for i in range(len(lolist)):
# 			self.containmentSolver.add(lolist[i])
# 			self.containmentSolver.add(uplist[i])
# 		if self.containmentSolver.check() == sat:
# 			self.containmentSolver.pop()
# 			return False
# 		else:
# 			self.containmentSolver.pop()
# 			return True

# 	def _checkIntersection(self,lo,up):
# 		lolist = []
# 		uplist = []
# 		for i in range(1,len(lo)):
# 			lolist.append(self.vardic['v'+str(i)]>=lo[i])
# 			uplist.append(self.vardic['v'+str(i)]<=up[i])
# 		self.intersectionSolver.push()
# 		for i in range(len(lolist)):
# 			self.intersectionSolver.add(lolist[i])
# 			self.intersectionSolver.add(uplist[i])
# 		#print self.intersectionSolver
# 		if self.intersectionSolver.check() == sat:
# 			self.intersectionSolver.pop()
# 			return True
# 		else:
# 			self.intersectionSolver.pop()
# 			return False


# 	def checkSimuTube(self,tube):
# 		for t in tube:
# 			ptList = []
# 			for i in range(1,len(t)):
# 				ptList.append(self.vardic['v'+str(i)]==t[i])
# 			self.intersectionSolver.push()
# 			for i in range(len(ptList)):
# 				self.intersectionSolver.add(ptList[i])
# 			if self.intersectionSolver.check() == sat:
# 				print t[0], self.intersectionSolver
# 				self.intersectionSolver.pop()
# 				return -1
# 			else:
# 				self.intersectionSolver.pop()
# 		return 1


# class PTChecker():
# 	def __init__(self):
# 		v1 = Real("v1")
# 		v2 = Real("v2")
# 		v3 = Real("v3")
# 		v4 = Real("v4")
# 		t = Real("t")
# 		self.varList = [t,v1,v2,v3,v4]		
# 		## Powertrain unsafe: there are four variables v1,v2,v3,v4
# 		## In mode Powerup, ( t>5 && v2 > 12.6) Or ( t>5 && v2 < 12.4) 
# 		## In mode Normal, ( t>5 && v2 > 14.8) Or ( t>5 && v2 < 14.6)
# 		## Don't have to check other modes
# 		self.pup_intSolver = Solver()
# 		self.nor_intSolver = Solver()
# 		self.pup_conSolver = Solver()
# 		self.nor_conSolver = Solver()

# 		pupUpper = 12.6
# 		pupLower = 12.4
# 		norUpper = 14.8
# 		norLower = 14.6
# 		#refine to get unsafe
# 		pupTime = 4.4
# 		norTime = 4.4

# 		#unsafe 
# 		# pupTime = 1
# 		# norTime = 1

# 		self.pup_intSolver.add(Or(And(t>pupTime,v2>pupUpper),And(t>pupTime,v2<pupLower)))
# 		self.nor_intSolver.add(Or(And(t>norTime,v2>norUpper),And(t>norTime,v2<norLower)))
# 		self.pup_conSolver.add(And(Not(And(t>pupTime,v2>pupUpper)),Not(And(t>pupTime,v2<pupLower))))
# 		self.nor_conSolver.add(And(Not(And(t>norTime,v2>norUpper)),Not(And(t>norTime,v2<norLower))))
# 		print "PowerUp", self.pup_intSolver,self.pup_conSolver
# 		print "Normal", self.nor_intSolver,self.nor_conSolver

# 	def checkSimuTube(self,tube,mode):
# 		if "Normal" in mode:
# 			curSolver = self.nor_intSolver
# 		elif "Power" in mode:
# 			curSolver = self.pup_intSolver
# 		else:
# 			return 1
# 		#print tube
# 		for t in tube:
# 			curSolver.push()
# 			curSolver.add(self.varList[0]==t[0])
# 			curSolver.add(self.varList[2]==t[2])

# 			if curSolver.check() == sat:
# 				print mode,curSolver
# 				curSolver.pop()
# 				return -1
# 			else:
# 				curSolver.pop()
# 		return 1

# 	def checkReachTube(self,tube,mode):
# 		safe = 1
# 		for i in range(0,len(tube),2):
# 			lower = tube[i]
# 			upper = tube[i+1]
# 			if self._checkIntersection(lower,upper,mode):
# 				if self._checkContainment(lower,upper,mode):
# 					print lower
# 					print upper
# 					return -1
# 				else:
# 					safe = 0
# 		return safe

# 	def _checkIntersection(self,lower,upper,mode):
# 		if "Normal" in mode:
# 			curSolver = self.nor_intSolver
# 		elif "Power" in mode:
# 			curSolver = self.pup_intSolver
# 		else:
# 			return False
# 		curSolver.push()
# 		curSolver.add(self.varList[0]>=lower[0])
# 		curSolver.add(self.varList[0]<=upper[0])
# 		curSolver.add(self.varList[2]>=lower[2])
# 		curSolver.add(self.varList[2]<=upper[2])

# 		if curSolver.check() == sat:
# 			curSolver.pop()
# 			return True
# 		else:
# 			curSolver.pop()
# 			return False

# 	def _checkContainment(self,lower,upper,mode):
# 		if "Normal" in mode:
# 			curSolver = self.nor_conSolver
# 		elif "Power" in mode:
# 			curSolver = self.pup_conSolver
# 		curSolver.push()
# 		curSolver.add(self.varList[0]>=lower[0])
# 		curSolver.add(self.varList[0]<=upper[0])
# 		curSolver.add(self.varList[2]>=lower[2])
# 		curSolver.add(self.varList[2]<=upper[2])

# 		if curSolver.check() == sat:
# 			curSolver.pop()
# 			return False
# 		else:
# 			curSolver.pop()
# 			return True




class uniformChecker():

	def __init__(self,dimension,unsafe):
		self.varDic = {'t':Real('t')}
		self.solverDic = {}
		for i in range(1,dimension+2):
			self.varDic['v' + str(i)] = Real('v' + str(i))
		for key in sorted(self.varDic)[::-1]:
			unsafe = self.replace(unsafe,key)
			#print key
			#print unsafe
		unsafeList = unsafe[1:].split('@')
		for unsafe in unsafeList:
			mode,con = unsafe.split(":")
			print con
			self.solverDic[mode] = [Solver(),Solver()]
			self.solverDic[mode][0].add(eval(con))
			self.solverDic[mode][1].add(eval(self._neg(con)))
			print mode
			print self.solverDic[mode][0]
			print self.solverDic[mode][1]
	
	def replace(self,unsafe,key):
		target = 'self.varDic["'+key+'"]'
		idxes = []
		for i in range(len(unsafe)):
			if unsafe[i:].startswith(key):
				idxes.append(i)

		for idx in idxes[::-1]:
			if idx!=0 and unsafe[idx-1] == '"':
				continue

			unsafe = unsafe[:idx] + target + unsafe[idx+len(key):]
		return unsafe



	def _neg(self,orig):
		def splitCondition(s):
			retval = []
			curbracket = 0
			lastSplit = 0
			s+=','
			for idx,c in enumerate(s):
				if c == '(':
					curbracket+=1
				elif c ==')':
					curbracket-=1
				elif c == ',' and curbracket==0:
					retval.append(s[lastSplit:idx])
					lastSplit = idx+1
			return retval
		if orig.startswith("And"):
			conditionList = splitCondition(orig[4:-1])
			newStr = "Or("
			for c in conditionList:
				newStr += 'Not('+c+'),'
			return newStr[:-1]+')'
		if orig.startswith("Or"):
			conditionList = splitCondition(orig[3:-1])
			newStr = "And("
			for c in conditionList:
				newStr += 'Not('+c+'),'
			return newStr[:-1]+')'

		return 'Not('+orig+')'

	def checkSimuTube(self,tube,mode):
		if mode in self.solverDic:
			curSolver = self.solverDic[mode][0]
		elif 'Allmode' in self.solverDic:
			curSolver = self.solverDic['Allmode'][0]
		else:
			return 1

		for t in tube:
			curSolver.push()
			curSolver.add(self.varDic['t'] == t[0])
			for i in range(1,len(t)):
				curSolver.add(self.varDic['v'+str(i)]==t[i])

			if curSolver.check() == sat:
				print mode,curSolver
				curSolver.pop()
				return -1
			else:
				curSolver.pop()
		return 1

	def checkReachTube(self,tube,mode):
		if not mode in self.solverDic and not 'Allmode' in self.solverDic:
			print 'No solver found for ', mode, "!!!!!!!"
			return 1

		safe = 1
		for i in range(0,len(tube),2):
			lower = tube[i]
			upper = tube[i+1]
			if self._checkIntersection(lower,upper,mode):
				#print "intersect at mode ",mode, lower,upper
				if self._checkContainment(lower,upper,mode):
					return -1
				else:
					safe = 0
		return safe

	def _checkIntersection(self,lower,upper,mode):
		if mode in self.solverDic:
			curSolver = self.solverDic[mode][0]
		elif 'Allmode' in self.solverDic:
			curSolver = self.solverDic['Allmode'][0]
		
		#print mode,lower[0],lower[2],upper[0],upper[2]
		curSolver.push()

		curSolver.add(self.varDic["t"]>=lower[0])
		curSolver.add(self.varDic["t"]<=upper[0])


		for i in range (1,len(lower)):
			curSolver.add(self.varDic["v"+str(i)]>=lower[i])
			curSolver.add(self.varDic["v"+str(i)]<=upper[i])

		if curSolver.check() == sat:
			curSolver.pop()
			return True
		else:
			curSolver.pop()
			return False

	def _checkContainment(self,lower,upper,mode):
		if mode in self.solverDic:
			curSolver = self.solverDic[mode][1]
		elif 'Allmode' in self.solverDic:
			curSolver = self.solverDic['Allmode'][1]

		curSolver.push()

		curSolver.add(self.varDic["t"]>=lower[0])
		curSolver.add(self.varDic["t"]<=upper[0])

		for i in range (1,len(lower)):
			curSolver.add(self.varDic["v"+str(i)]>=lower[i])
			curSolver.add(self.varDic["v"+str(i)]<=upper[i])

		if curSolver.check() == sat:
			curSolver.pop()
			return False
		else:
			curSolver.pop()
			return True


