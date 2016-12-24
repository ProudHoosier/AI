import solver
class WumpusMDP:
	# wall_locations is a list of (x,y) pairs
	# pit_locations is a list of (x,y) pairs
	# wumnpus_location is an (x,y) pair
	# gold_location is an (x,y) pair
	# start_location is an (x,y) pair representing the start location of the agent


	def __init__(self, wall_locations, pit_locations, wumpus_location, gold_location, start_location):
		self.wall_locations = wall_locations
		self.pit_locations = pit_locations
		self.wumpus_location = wumpus_location
		self.gold_location = gold_location
		self.start_location = start_location
		self.space = []
		
	def A(self):
		# return list of actions
		return ['do nothing', 'left', 'right', 'up', 'down', 'shoot left', 'shoot right', 'shoot up', 'shoot down'] 

	def S(self):
		x = []
		y = []
		for s in self.wall_locations:
			x.append(s[0])
			y.append(s[1])
		
		self.width = max(x) - min(x)
		self.height = max(y) - min(y)
		#(x,y,arrow,wumpus)
		for x in range(0, self.width+1):
			for y in range(0, self.height+1):
				#if(x,y) not in self.wall_locations:
				self.space.append((x, y, True, True))
				self.space.append((x, y, False, True))
				self.space.append((x, y, False, False))
			
		# return list of states
		#print(space)
		return self.space

	def P(self, s, a, u):
		# return probability of transitioning from state s to state u when taking action a
		if s == u and a == 'do nothing':
			return 1
			
		if a in ['left', 'right', 'up', 'down'] and s[2] == u[2] and s[3] == u[3]:
			if s == u:
				if self.isWall(s, a):
					return 0.9
				if self.isIntended(s, a, u):
					return 0.1/3
			else:
				if self.isIntended(s, a, u):
					return 0.9
				else:
					return 0.1/3
					
		if a in ['shoot left', 'shoot right', 'shoot up', 'shoot down'] and (s[0],s[1]) == (u[0],u[1]) and not s[2]:
			if not s[2] and not s[3]:
				return 1
			if not s[2] and s[3]:
				return 1
			
		else:
			return 0
		
		

	def isIntended(self, s, a, u):
		if a == 'left':
			if u == (s[0]-1, s[1]):
				return True
		elif a == 'right':
			if u == (s[0]+1, s[1]):
				return True
		elif a == 'up':
			if u == (s[0], s[1]+1):
				return True
		elif a == 'down':
			if u == (s[0], s[1]-1):
				return True
		else:
			return False
				
	def isWall(self, s, a):
		if a == 'left':
			if (s[0]-1, s[1]) in  self.wall_locations:
				return True
		elif a == 'right':
			if (s[0]+1, s[1]) in  self.wall_locations:
				return True
		elif a == 'up':
			if (s[0], s[1]+1) in  self.wall_locations:
				return True
		elif a == 'down':
			if (s[0], s[1]-1) in  self.wall_locations:
				return True
		else:
			return False

	def R(self, s):
		# return reward for state s
		if s in self.pit_locations:
			return -100
		elif s == self.wumpus_location and not s[3]:
			return -100
		elif s == self.gold_location:
			return 100
		else:
			return -1
		#return self.reward
		
	def initial_state(self):
		return self.start_location # return initial state

	def gamma(self):
		return 0.99

# EXAMPLE USAGE:
# mdp = WumpusMDP([(0,0),(1,0),(2,0),(3,0),(3,1),(3,2),(3,3),(2,3),(1,3),(0,3),(0,2),(0,1)], [(1,2)], (2,1), (2,2), (1,1))
