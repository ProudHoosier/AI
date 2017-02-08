from copy import deepcopy
from itertools import chain

## This module uses dpll algorithm to find out if a given logical statement is solvable.
class Solver:
	'''Initialize the solver instance with cluases in Conjunctive normal form.
	Collect all the atomic symbols from these clauses
	'''
	def __init__(self, cnf):
		self.clauses = cnf
		merged_clauses = list(chain(*self.clauses))
		self.symbolsbols = set([c for c in merged_clauses if c > 0])|set([abs(c) for c in merged_clauses if c < 0])

	def solve(self):	
		return self.dpll(self.clauses, self.symbolsbols)

	# Method which performs reductions based on unit clause and positive literals.	
	def reduce(self, var, temp):
		tempclauses = deepcopy(temp)
		
		for clause in temp:
			if var in c:
				tempclauses.remove(clause)
			if -var in c:
				tempclauses[tempclauses.index(clause)].remove(-var)

		return tempclauses

	
	def dpll(self, clauses, symbols):
		for clause in clauses:
			if len(clause) == 1:
				literal = list(clause)[0]
				alpha = clauses[:]
				s = symbols.copy()
				for clause in clauses:
					if literal in clause:
						alpha.remove(clause)
					if -literal in clause:
						alpha[alpha.index(clause)].remove(-P)
				if abs(literal) in symbols:
					s.remove(abs(literal))					
				 
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

		reduced1 = self.reduce(uvar, clauses)
		reduced2 = self.reduce(-uvar, newclauses)
		
		return self.dpll(reduced1, literals) or self.dpll(reduced2, literals)
