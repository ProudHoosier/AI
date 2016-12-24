import random
import math

class Solver:
	def __init__(self, mdp):
		# any initialisation you might like
		self.mdp = mdp
		self.states = self.mdp.S()
		self.actions = self.mdp.A()
		self.gamma = self.mdp.gamma()
		self.theta = 0.001
		self.V = {}
		self.policy = {}
	
	def solve(self):
		self.value_iteration()
		#print('policy', self.policy)
		return self.policy
	
	def value_iteration(self):
		#Solving an MDP by value iteration.
		self.V = dict([(s, 0) for s in self.states])
		while True:
			delta = 0
			for s in self.states:
				#print('inside value_iteration')
				v = self.V[s]
				maxi = -math.inf
				best_action = ''
				for action in self.actions:
					current = self.total(s, action)
					if maxi < current:
						maxi = current
						print('best action', best_action)
						best_action = action
				self.V[s] = maxi
				self.policy[s] = best_action			
				delta = max(delta, abs(v - self.V[s]))
		
			if delta < self.theta:
				return
					
						
	def total(self, state, action):
		total = 0		
		for s1 in self.states:
			total += self.mdp.P(state, action, s1) * (self.mdp.R(s1) + self.gamma * self.V[s1])
		#print('total', total)
		return total

		
		
		
		
		