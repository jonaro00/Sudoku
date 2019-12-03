import random
import time

class Sudoku:

	one_to_nine = [i for i in range(1,10)]
	section_indicies = {0:(0,3,0,3),1:(0,3,3,6),2:(0,3,6,9),3:(3,6,0,3),4:(3,6,3,6),5:(3,6,6,9),6:(6,9,0,3),7:(6,9,3,6),8:(6,9,6,9)}

	def __init__(self, debug=False):
		self.board = self.new_board()
		self.arrange_tile_groups()
		self.generate(debug)


	@property
	def board2Dlist(self):
		return [[t.value for t in r] for r in self.board]


	@staticmethod
	def new_board():
		return tuple(tuple(Sudoku.Tile() for __ in range(9)) for _ in range(9))


	def arrange_tile_groups(self):
		self.rows = tuple(Sudoku.Row(*r) for r in self.board)
		self.cols = tuple(Sudoku.Col(*tuple(r[c] for r in self.board)) for c in range(9))
		self.secs = []
		for s in range(9):
			i, j, k, l = self.section_indicies[s]
			sec = []
			for r in range(i,j):
				sec.extend(self.board[r][k:l])
			self.secs.append(sec)
		self.secs = tuple(Sudoku.Sec(*s) for s in self.secs)


	@staticmethod
	def section_index(row_index, col_index):
		return col_index // 3 + row_index // 3 * 3


	def generate(self, debug=False):
		for i in (0, 3, 6): # 
			while True:
				for j in range(9):
					try:
						x = self.get_entries_left(i, j)
						self.board[i][j].value = random.choice(x)
					except IndexError:
						for t in self.rows[i]:
							t.value = 0
						break
					if debug: self.print_board()
				else:
					if self.soft_valid():
						break
		while True:
			for i in (1, 2, 4, 5, 7, 8): # , 3, 6
				for j, t in enumerate(self.rows[i]):
					t.can_be = self.get_entries_left(i, j) if t.value == 0 else []
			can_be = []
			can_be_len = [[c if c > 0 else 10 for c in [len(c) for c in r]] for r in can_be]
			fewest_index = [0, 0]
			row_contains_min = 0
			for r in can_be_len:
				if min(r) < min(can_be_len[row_contains_min]):
					row_contains_min = can_be_len.index(r)
			fewest_index[0] = row_contains_min
			fewest_index[1] = can_be_len[row_contains_min].index(min(can_be_len[row_contains_min]))
			
			self.board[fewest_index[0]][fewest_index[1]] = random.choice(can_be[fewest_index[0]][fewest_index[1]])
			
			if debug: self.print_board()
			
			if self.hard_valid():
				return True
		return False

	def get_entries_left(self, row_index, col_index):

		r = set(self.rows[row_index].entries_left)
		c = set(self.cols[col_index].entries_left)
		s = set(self.secs[self.section_index(row_index,col_index)].entries_left)
		return list(set.intersection(r,c,s))

		# def get_row_entries_left(board, row_index):
		# 	return [n for n in Sudoku.one_to_nine if n not in board[row_index]]

		# def get_col_entries_left(board, col_index):
		# 	col = [row[col_index] for row in board]
		# 	return [n for n in Sudoku.one_to_nine if n not in col]

		# def get_sec_entries_left(board, row_index, col_index):
		# 	sec_index = col_index // 3 + row_index // 3 * 3
		# 	i, j, k, l, = Sudoku.section_indicies[sec_index]
		# 	sec = []
		# 	for r in range(i,j):
		# 		sec.extend(board[r][k:l])
		# 	return [n for n in Sudoku.one_to_nine if n not in sec]

		# r = get_row_entries_left(board, row_index)
		# c = get_col_entries_left(board, col_index)
		# s = get_sec_entries_left(board, row_index, col_index)
		


		# board = []
		# for _ in range(9):
		# 	board.append([0]*9)
		# for i, r in enumerate(board):
		# 	if i in [0, 1, 2, 3, 6]:
		# 		while True:
		# 			for j, c in enumerate(r):
		# 				try:
		# 					x = get_entries_left(board, i, j)
		# 					board[i][j] = random.choice(x)
		# 				except IndexError:
		# 					board[i] = [0]*9
		# 					break
		# 				if debug: Sudoku.print_board(board)
		# 			else:
		# 				if Sudoku.soft_valid(board):
		# 					break
		# 	else: # 4, 5, 7, 8
		# 		can_be = []
		# 		for _ in range(9):
		# 			can_be.append([])
		# 		while board[i].count(0) > 0:
		# 			for j, c in enumerate(r):
		# 				can_be[j] = get_entries_left(board, i, j) if board[i][j] == 0 else []
		# 			can_be_len = [c if c > 0 else 10 for c in [len(c) for c in can_be]]
		# 			fewest_index = can_be_len.index(min(can_be_len))
		# 			board[i][fewest_index] = random.choice(can_be[fewest_index])
		# 			if debug: Sudoku.print_board(board)

		# return board


		# board = []
		# for _ in range(9):
		# 	board.append([0]*9)
		# for i, r in enumerate(board):
		# 	while True:
		# 		for j, c in enumerate(r):
		# 			try:
		# 				x = get_entries_left(board, i, j)
		# 				board[i][j] = random.choice(x)
		# 			except IndexError:
		# 				board[i] = [0]*9
		# 				break
		# 			if debug:
		# 				print('')
		# 				for r in board:
		# 					print(''.join(str(r)).replace('0',' '))
		# 		else:
		# 			if Sudoku.soft_valid(board):
		# 				break




		# board = []
		# for _ in range(9):
		# 	board.append([0]*9)
		# for i, r in enumerate(board):
		# 	row_entries = [_ for _ in range(1,10)]
		# 	while True:
		# 		random.shuffle(new_entries)
		# 		board[i] = new_entries
		# 		if debug:
		# 			print('\n')
		# 			for r in board:
		# 				print(''.join(str(r)).replace('0',' '))
		# 		if Sudoku.board_valid(board):
		# 			break



				# while True:
				# 	board[i][j] = random.randint(1,9)
				# 	if Sudoku.board_valid(board): break
				# if debug:
				# 	print('\n')
				# 	for r in board:
				# 		print(''.join(str(r)).replace('0',' '))
				
				# i % 3
				# j / 3
				# rand_pool = []


	def solve(self):
		pass


	def rows_soft_valid(self):
		for row in self.rows:
			if not row.soft_valid():
				return False
		return True

	def cols_soft_valid(self):
		for col in self.cols:
			if not col.soft_valid():
				return False
		return True

	def secs_soft_valid(self):
		for sec in self.secs:
			if not sec.soft_valid():
				return False
		return True

	def soft_valid(self):
		if self.rows_soft_valid() and self.cols_soft_valid() and self.secs_soft_valid():
			return True
		return False

	def rows_hard_valid(self):
		for row in self.rows:
			if not row.hard_valid(): 
				return False
		return True

	def cols_hard_valid(self):
		for col in self.cols:
			if not col.hard_valid(): 
				return False
		return True

	def secs_hard_valid(self):
		for sec in self.secs:
			if not sec.hard_valid(): 
				return False
		return True

	def hard_valid(self):
		if self.rows_hard_valid() and self.cols_hard_valid() and self.secs_hard_valid():
			return True
		return False


	def print_board(self):
		print('_'*27)
		print(str(self.board2Dlist).replace('],',']\n').replace('[[','[').replace(' [','[').replace(']]',']').replace(',',' ').replace('0',' ').replace('[','|').replace(']','|'))
		print('▔'*26)
	
	def print_list(self):
		print(str(self.board2Dlist).replace('],','],\n'))

	class Tile:
		def __init__(self):
			self.value = 0
			self.can_be = []

		def __repr__(self):
			return f'<Tile:{self.value}>'
	
	class TileGroup:
		def __init__(self, *tiles):
			self.tiles = tiles

		def __repr__(self):
			return f'<TileGroup:{str(self.values)}>'
		
		def __iter__(self):
			return iter(self.tiles)
		
		@property
		def values(self):
			return [t.value for t in self.tiles]
		
		@property
		def entries_left(self):
			return [n for n in Sudoku.one_to_nine if n not in self.values]
		
		def soft_valid(self):
			for i in Sudoku.one_to_nine:
				if self.values.count(i) > 1:
					return False
			return True
		
		def hard_valid(self):
			if sorted(self.values) == Sudoku.one_to_nine:
				return True
			return False

	class Row(TileGroup):
		def __repr__(self):
			return f'<Row:{str(self.values)}>'

	class Col(TileGroup):
		def __repr__(self):
			return f'<Col:{str(self.values)}>'

	class Sec(TileGroup):
		def __repr__(self):
			return f'<Sec:{str(self.values)}>'


# t0 = time.time()
# success = 0
# for _ in range(1000):
# 	try:
# 		if Sudoku.generate():
# 			success += 1
# 	except:
# 		pass
# print(success)
# t1 = time.time()
# print(t1-t0, 'seconds')

t0 = time.time()
sud = Sudoku(debug=True)
t1 = time.time()
print('Generated Sudoku in:', t1-t0, 'seconds')
sud.print_board()

# test_sudoku = [
# 	[8,0,0,0,0,0,7,0,0],
# 	[0,9,1,0,3,5,0,2,0],
# 	[7,0,0,0,4,0,3,0,0],
# 	[0,2,0,5,6,0,0,0,4],
# 	[0,3,0,0,9,0,0,6,0],
# 	[9,0,0,0,1,2,0,8,0],
# 	[0,0,9,0,8,0,0,0,7],
# 	[0,4,0,2,7,0,6,9,0],
# 	[0,0,7,0,0,0,0,0,2]
# ]
first_sudoku = [
	[1, 6, 3, 2, 9, 4, 8, 7, 5],
	[7, 8, 5, 1, 3, 6, 9, 2, 4],
	[9, 4, 2, 7, 5, 8, 1, 3, 6],
	[4, 2, 8, 5, 1, 3, 7, 6, 9],
	[5, 9, 7, 8, 6, 2, 4, 1, 3],
	[6, 3, 1, 9, 4, 7, 2, 5, 8],
	[2, 1, 4, 3, 8, 5, 6, 9, 7],
	[8, 5, 9, 6, 7, 1, 3, 4, 2],
	[3, 7, 6, 4, 2, 9, 5, 8, 1]
]


#print(Sudoku.hard_valid(first_sudoku))