import random
import time

class Sudoku(object):

	one_to_nine = [_ for _ in range(1,10)]

	@staticmethod
	def generate(debug=False):

		def get_row_entries_left(board, row_index):
			return [n for n in Sudoku.one_to_nine if not n in board[row_index]]


		def get_col_entries_left(board, col_index):
			col = [row[col_index] for row in board]
			return [n for n in Sudoku.one_to_nine if not n in col]


		def get_sec_entries_left(board, row_index, col_index):
			sec_index = col_index // 3 + row_index // 3 * 3
			i, j, k, l, = Sudoku.sections[str(sec_index)]
			sec = []
			for r in range(i,j):
				sec.extend(board[r][k:l])
			return [n for n in Sudoku.one_to_nine if not n in sec]


		def get_entries_left(board, row_index, col_index):
			r = get_row_entries_left(board, row_index)
			c = get_col_entries_left(board, col_index)
			s = get_sec_entries_left(board, row_index, col_index)
			return [n for n in Sudoku.one_to_nine if n in r and n in c and n in s]


		board = []
		for _ in range(9):
			board.append([0]*9)
		for i in [0]: # , 3, 6
			while True:
				for j, c in enumerate(board[i]):
					try:
						x = get_entries_left(board, i, j)
						board[i][j] = random.choice(x)
					except IndexError:
						board[i] = [0]*9
						break
					if debug: Sudoku.print_board(board)
				else:
					if Sudoku.soft_valid(board):
						break
		can_be = []
		for _ in range(9):
			can_be.append([])
			for __ in range(9):
				can_be[-1].append([])
		while True:
			for i in [1, 2, 3, 4, 5, 6, 7, 8]: # 
				for j, c in enumerate(board[i]):
					can_be[i][j] = get_entries_left(board, i, j) if board[i][j] == 0 else []
			can_be_len = [[c if c > 0 else 10 for c in [len(c) for c in r]] for r in can_be]
			fewest_index = [None, None]
			contains_min = 0
			for r in can_be_len:
				if min(r) < min(can_be_len[contains_min]):
					contains_min = can_be_len.index(r)
			fewest_index[0] = contains_min
			fewest_index[1] = can_be_len[contains_min].index(min(can_be_len[contains_min]))
			
			board[fewest_index[0]][fewest_index[1]] = random.choice(can_be[fewest_index[0]][fewest_index[1]])
			
			if debug: Sudoku.print_board(board)
			
			if Sudoku.hard_valid(board):
				return board

		


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



	@staticmethod
	def solve(parameter_list):
		pass


	sections = {"0":(0,3,0,3),"1":(0,3,3,6),"2":(0,3,6,9),"3":(3,6,0,3),"4":(3,6,3,6),"5":(3,6,6,9),"6":(6,9,0,3),"7":(6,9,3,6),"8":(6,9,6,9)}
	
	@staticmethod
	def rows_soft_valid(board):
		for row in board:
			for i in range(1,10):
				if row.count(i) > 1:
					return False
		return True


	@staticmethod
	def cols_soft_valid(board):
		for c in range(len(board[0])):
			col = [row[c] for row in board]
			for i in range(1,10):
				if col.count(i) > 1:
					return False
		return True


	@staticmethod
	def secs_soft_valid(board):
		for s in range(9):
			i, j, k, l = Sudoku.sections[str(s)]
			sec = []
			for r in range(i,j):
				sec.extend(board[r][k:l])
			for i in range(1,10):
				if sec.count(i) > 1:
					return False
		return True


	@staticmethod
	def soft_valid(board):
		if Sudoku.rows_soft_valid(board) and Sudoku.cols_soft_valid(board) and Sudoku.secs_soft_valid(board):
			return True
		return False

	
	@staticmethod
	def rows_hard_valid(board):
		for row in board:
			r = row[:]
			r.sort()
			if r != Sudoku.one_to_nine: 
				return False
		return True


	@staticmethod
	def cols_hard_valid(board):
		for c in range(len(board[0])):
			col = [row[c] for row in board]
			col.sort()
			if col != Sudoku.one_to_nine:
				return False
		return True


	@staticmethod
	def secs_hard_valid(board):
		for s in range(9):
			i, j, k, l = Sudoku.sections[str(s)]
			sec = []
			for r in range(i,j):
				sec.extend(board[r][k:l])
			sec.sort()
			if sec != Sudoku.one_to_nine:
				return False
		return True


	@staticmethod
	def hard_valid(board):
		if Sudoku.rows_hard_valid(board) and Sudoku.cols_hard_valid(board) and Sudoku.secs_hard_valid(board):
			return True
		return False

	
	@staticmethod
	def print_board(board):
		print('')
		print('_'*27)
		print(str(board).replace('],',']\n').replace('[[','[').replace(' [','[').replace(']]',']').replace(',',' ').replace('0',' ').replace('[','|').replace(']','|'))
		print('▔'*26)

	
	@staticmethod
	def print_list(board):
		print('')
		print(str(board).replace('],','],\n'))

t0 = time.time()
sud = Sudoku.generate(debug=True)
t1 = time.time()
print('Generated Sudoku in:', t1-t0, 'seconds')
Sudoku.print_board(sud)

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