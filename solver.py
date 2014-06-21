import time, sys

with open('sudoku.in', 'r') as dump:
	data = enumerate(map(int, list(dump.read()[:-1])))

space = set(xrange(1, 10))

class Cell:
	
	def __init__(self, c):
		self.value = c[1]
		self.xy = (c[0] / 9, c[0] % 9)
		self.possible = None

class Sudoku:
	
	def __init__(self, sudoku):
		self.board = [Cell(c) for c in sudoku]
		self.changed = True
	
	def set_certain(self):
		for c in [c for c in self.board if not c.value]:
			c.possible = space - self.possible(c.xy)
			if len(c.possible) == 1:
				c.value = c.possible.pop()
				self.changed = True
			elif len(c.possible) == 0:
				return 0
	
	def possible(self, p):
		return set([self.board[p[0] * 9 + x].value for x in xrange(9)] + [self.board[x * 9 + p[1]].value for x in xrange(9)] + [self.board[x * 9 + y].value for x in xrange(p[0] / 3 * 3, (p[0] / 3 + 1) * 3) for y in xrange(p[1] / 3 * 3, (p[1] / 3 + 1) * 3)])
	
	def solve(self):
		while self.changed:
			self.changed = False
			if self.set_certain() == 0:
				return 0
		
		return 1
	
	def solved(self):
		for _ in self.board:
			if not _.value:
				return 0
				
		return 1
	
	def min_possible(self):
		return min([_ for _ in self.board if not _.value], key = lambda _: len(_.possible))
	
	def data(self):
		return list(enumerate([_.value for _ in self.board]))
	
	def print_board(self):
		for x in xrange(9):
			for y in xrange(9):
				print self.board[9 * x + y].value,
			print '\n'

class Solver:
	
	def __init__(self, d):
		self.start = time.time()
		self.tree = [Sudoku(d)]
		self.count = -1
		self.run()
		
	def run(self):
		while 1:
			self.count += 1
			
			if self.tree[-1].solve():
				if self.tree[-1].solved():
					print 'Time taken: {} seconds.\nAssumptions made {}.\n'.format(time.time() - self.start, self.count)
					self.tree[-1].print_board()
					del self.tree
					break
			else:
				del self.tree[-1]
			
			while self.tree and not self.tree[-1].min_possible().possible:
				del self.tree[-1]
			else:
				if not self.tree:
					sys.exit('Sudoku cannot be solved!')
			
			d = self.tree[-1].data()
			c = self.tree[-1].min_possible()
			d[c.xy[0] * 9 + c.xy[1]] = (c.xy[0] * 9 + c.xy[1], c.possible.pop())
			self.tree.append(Sudoku(d))

Solver(data)
