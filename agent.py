import random
import dpll
import copy
import pycosat

class Agent:
	def __init__(self):
		self.location = ()
		self.wumpus_killed = False
		self.KB = []
		self.history = []
		self.explored = set([])
		self.walls = set([])
		self.counter = 0
		self.no_arraow = False
		
		one_wumpus = set([])
		for i in range (1,21):
			for j in range(1,21):
					val = int(str(-4) + str(100*i + j))
					one_wumpus.add(val)	
		
		for a in one_wumpus:
			for b in one_wumpus:
				if a > b:
					self.KB.append({a,b})
		
		print('initial KB:', len(self.KB))
		
	def hash(self, x, y):
		if x in range(1,21) and y in range(1,21):
			return str(x*100 + y)
		else:
			return None
	
	#Create only one wumpus rule in world
	
	def get_action(self):
		actions = ['MOVE_UP', 'MOVE_DOWN', 'MOVE_LEFT', 'MOVE_RIGHT']
		extras = ['SHOOT_UP', 'SHOOT_DOWN', 'SHOOT_LEFT', 'SHOOT_RIGHT']
		self.no_arraow = False
		'''
		Px;y is true <=> there is a pit in position (x; y)
		Bx;y is true <=> there is a breeze in position (x; y)
		Sx;y is true <=> there is a stench in position (x; y)
		Wx;y is true <=> there is a wumpus in position (x; y)
		
		Breeze - 1, Stench - 2, Pit - 3, wumpus - 4, wall -5
		'''
		
		self.explored.add(self.location)
		
		i = self.location[0]
		j = self.location[1]
		left = (i-1,j)
		right = (i+1,j)
		up = (i,j+1)
		down = (i,j-1)
		moves = [up,down,left,right]
		possible_moves = []
		
		for move in moves:
			isPit,isWumpus = None,None
			shoot,action = None,None
			#if move not in self.history:
			alpha = set()
			#print('walls', self.walls)
			if self.hash(move[0],move[1]) and move not in self.walls and self.counter < 1000:
				alpha = set()
				alpha.add(-int('4'+ self.hash(move[0],move[1])))
				#print('alpha', alpha)
				isWumpus = self.ask(alpha)
				#print('wumpus?',isWumpus)
				alpha = set()
				alpha.add(int('3'+ self.hash(move[0],move[1])))
				alpha.add(int('4'+ self.hash(move[0],move[1])))
				isSafe = self.ask(alpha)
				#print('wumpus?',isSafe)
				alpha = set()
				alpha.add(int('3'+ self.hash(move[0],move[1])))
				isPit = self.ask(alpha)
				#print('Pit?',isPit)

				if not self.wumpus_killed:
					if isWumpus == 'UNSAT':
						if move == up:
							shoot = extras[0]
						elif move == down:
							shoot = extras[1]
						elif move == left:
							shoot = extras[2]
						elif move == right:
							shoot = extras[3]
						self.no_arraow = True
						return shoot

					elif isSafe == 'UNSAT':
						
						if move not in self.explored:
							self.history.append(move)
							return self.find_action(move)
						else:
							possible_moves.append(move)
		
				else:
					#print('entered pit logic')
					if isPit == 'UNSAT':
						if move not in self.explored:
							self.history.append(move)
							return self.find_action(move)
						else:
							possible_moves.append(move)

		if possible_moves:
			loc = random.choice(possible_moves)
			action = self.find_action(loc)
			self.history.append(loc)
			return action										
		else:
			return 'QUIT'
				
	def find_action(self,move):
		if move[0] == self.location[0]:
			if move[1] - self.location[1]== 1:
				return 'MOVE_UP'
			else:
				return 'MOVE_DOWN'
		else:
			if move[0] - self.location[0] == 1:
				return 'MOVE_RIGHT'
			else:
				return 'MOVE_LEFT'

	def ask(self, alpha):
		tempkb = self.KB[:]
		tempkb.append(alpha)
		d = pycosat.solve(tempkb)
		return d

	def neighbors(self, loc):    # returns neighbours of tuple loc = (x,y) 
		all_neighbors = [self.hash(loc[0]+1,loc[1]), self.hash(loc[0]-1,loc[1]), self.hash(loc[0],loc[1]+1), self.hash(loc[0],loc[1]-1)]
		valid = []
		for x in all_neighbors:
			if x:
				valid.append(x)
		return valid

	def give_senses(self, location, breeze, stench):

		if self.location == location and not self.no_arraow:
			self.walls.add(self.history[-1])
			self.explored.add(location)
		#no pit and no wumpus in this location if we have come here.
		
		if location in self.explored:
			self.counter += 1
		else:
			self.counter = 0
			self.explored.add(location)

		self.location = location
		if not self.wumpus_killed:
			self.KB.append({-int('3' + self.hash(location[0],location[1]))})
			self.KB.append({-int('4' + self.hash(location[0],location[1]))})
			#self.KB.append(set([-int('5' + self.hash(i,j))]))
		neighbors = self.neighbors(self.location)

		if breeze:
			clause = set()
			for tile in neighbors:
				if tile:
					clause.add(int('3' + tile))
			if clause not in self.KB:
				self.KB.append(clause)
			
		if stench:
			clause = set()
			for tile in neighbors:
				if tile:
					clause.add(int('4' + tile))
			if clause not in self.KB:
				self.KB.append(clause)
			
		if not breeze:
			for tile in neighbors:
				val = int('-3' + tile)
				if {val} not in self.KB:
					self.KB.append({val})
		
		if not stench:
			for tile in neighbors:
				val = int('-4' + tile)
				if {val} not in self.KB:
					self.KB.append({val})
	
		#print(len(self.KB))

	def killed_wumpus(self):
		self.wumpus_killed = True
		print('killed it')


