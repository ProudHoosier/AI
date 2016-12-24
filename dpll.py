from copy import deepcopy
from itertools import chain

class Solver:
	def __init__(self, cnf):
		self.clauses = cnf
		merged_clauses = list(chain(*self.clauses))
		self.symbolsbols = set([c for c in merged_clauses if c > 0])|set([abs(c) for c in merged_clauses if c < 0])

	def solve(self):	
		return self.dpll(self.clauses,self.symbolsbols)

		
	def reduce(self, var, temp):
		#print("Within reduce",temp)
		tempclauses = deepcopy(temp)
		
		for c in temp:
			if var in c:
				tempclauses.remove(c)
			if -var in c:
				tempclauses[tempclauses.index(c)].remove(-var)

		return tempclauses

	
	def dpll(self, clauses, symbols):
		for c in clauses:
			if len(c) == 1:
				P = list(c)[0]
				#print ("p is:",P)
				alpha = clauses[:]
				s = symbols.copy()
				for c in clauses:
					if P in c:
						alpha.remove(c)
					if -P in c:
						alpha[alpha.index(c)].remove(-P)
				if abs(P) in symbols:
					s.remove(abs(P))					
				 
				symbols = s
				clauses = alpha
		
		if not clauses:
			return True
		
		for c in clauses:
			if len(c) == 0:
				return False

		newclauses = clauses[:]
		literals = symbols.copy()		
		freq = {}
		
		#Initialize freq for each literal
		for literal in literals:
			freq[literal] = 0
		
		for clause in clauses:
			for literal in literals:
				if literal in clause:
					freq[literal] += 1

		most_freq = freq[literal]
		
		for literal in literals:
			if freq[literal] >= most_freq:
				most_freq = freq[literal]
				uvar = literal

		
		literals.remove(abs(uvar))

		reduced1 = self.reduce(uvar,clauses)
		reduced2 = self.reduce(-uvar,newclauses)
		
		return self.dpll(reduced1, literals) or self.dpll(reduced2, literals)
