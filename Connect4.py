import numpy as np
import random
import pygame as pg
import sys
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

DIFFICULTY = 7

ROWS = 6
COLUMNS = 7

PLAYER = 0
AI = 1

INFINITY = math.inf

EMPTY_PIECE = 0
PLAYER_PIECE = 1
AI_PIECE = 2

CONNECTION_SIZE = 4
BOX_SIZE = 150

def create_game_board():
	game_board = np.zeros((ROWS, COLUMNS))
	return game_board

def print_game_board(game_board):
	print(np.flip(game_board, 0))

def set_piece(game_board, row, col, piece):
	game_board[row][col] = piece

def is_valid_move(game_board, col):
	return game_board[ROWS-1][col] == 0

def get_row_location(game_board, col):
	for r in range(ROWS):
		if game_board[r][col] == 0:
			return r

def winning_move(game_board, piece):
	for c in range(COLUMNS-3):
		for r in range(ROWS):
			if game_board[r][c] == piece and game_board[r][c+1] == piece and game_board[r][c+2] == piece and game_board[r][c+3] == piece:
				return True

	for c in range(COLUMNS):
		for r in range(ROWS-3):
			if game_board[r][c] == piece and game_board[r+1][c] == piece and game_board[r+2][c] == piece and game_board[r+3][c] == piece:
				return True

	for c in range(COLUMNS-3):
		for r in range(ROWS-3):
			if game_board[r][c] == piece and game_board[r+1][c+1] == piece and game_board[r+2][c+2] == piece and game_board[r+3][c+3] == piece:
				return True

	for c in range(COLUMNS-3):
		for r in range(3, ROWS):
			if game_board[r][c] == piece and game_board[r-1][c+1] == piece and game_board[r-2][c+2] == piece and game_board[r-3][c+3] == piece:
				return True

def set_score(series, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if series.count(piece) == 4:
		score += 100
	elif series.count(piece) == 3 and series.count(EMPTY_PIECE) == 1:
		score += 10
	elif series.count(piece) == 2 and series.count(EMPTY_PIECE) == 2:
		score += 4

	if series.count(opp_piece) == 3 and series.count(EMPTY_PIECE) == 1:
		score -= 8

	return score

def find_best_score(game_board, piece):
	score = 0

	center_array = [int(i) for i in list(game_board[:, COLUMNS//2])]
	center_count = center_array.count(piece)
	score += center_count * 6

	for r in range(ROWS):
		row_array = [int(i) for i in list(game_board[r,:])]
		for c in range(COLUMNS-3):
			series = row_array[c:c+CONNECTION_SIZE]
			score += set_score(series, piece)

	for c in range(COLUMNS):
		col_array = [int(i) for i in list(game_board[:,c])]
		for r in range(ROWS-3):
			series = col_array[r:r+CONNECTION_SIZE]
			score += set_score(series, piece)

	for r in range(ROWS-3):
		for c in range(COLUMNS-3):
			series = [game_board[r+i][c+i] for i in range(CONNECTION_SIZE)]
			score += set_score(series, piece)

	for r in range(ROWS-3):
		for c in range(COLUMNS-3):
			series = [game_board[r+3-i][c+i] for i in range(CONNECTION_SIZE)]
			score += set_score(series, piece)

	return score

def is_terminal_node(game_board):
	return winning_move(game_board, PLAYER_PIECE) or winning_move(game_board, AI_PIECE) or len(get_valid_locations(game_board)) == 0

def minimax(game_board, depth, alpha, beta, maximizing_score):
	valid_locations = get_valid_locations(game_board)
	is_terminal = is_terminal_node(game_board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(game_board, AI_PIECE):
				return (None, INFINITY)
			elif winning_move(game_board, PLAYER_PIECE):
				return (None, -INFINITY)
			else:
				return (None, 0)
		else:
			return (None, find_best_score(game_board, AI_PIECE))
	if maximizing_score:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_row_location(game_board, col)
			b_copy = game_board.copy()
			set_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else:
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_row_location(game_board, col)
			b_copy = game_board.copy()
			set_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(game_board):
	valid_locations = []
	for col in range(COLUMNS):
		if is_valid_move(game_board, col):
			valid_locations.append(col)
	return valid_locations

def select_best_move(game_board, piece):

	valid_locations = get_valid_locations(game_board)
	best_score = -99999
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_row_location(game_board, col)
		temp_game_board = game_board.copy()
		set_piece(temp_game_board, row, col, piece)
		score = find_best_score(temp_game_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

def draw_game_board(game_board):
	for c in range(COLUMNS):
		for r in range(ROWS):
			pg.draw.rect(screen, BLUE, (c*BOX_SIZE, r*BOX_SIZE+BOX_SIZE, BOX_SIZE, BOX_SIZE))
			pg.draw.circle(screen, WHITE, (int(c*BOX_SIZE+BOX_SIZE/2), int(r*BOX_SIZE+BOX_SIZE+BOX_SIZE/2)), RADIUS)
	
	for c in range(COLUMNS):
		for r in range(ROWS):
			if game_board[r][c] == PLAYER_PIECE:
				pg.draw.circle(screen, RED, (int(c*BOX_SIZE+BOX_SIZE/2), height-int(r*BOX_SIZE+BOX_SIZE/2)), RADIUS)
			elif game_board[r][c] == AI_PIECE: 
				pg.draw.circle(screen, YELLOW, (int(c*BOX_SIZE+BOX_SIZE/2), height-int(r*BOX_SIZE+BOX_SIZE/2)), RADIUS)
	pg.display.update()

game_board = create_game_board()
game_ends = False

pg.init()

width = COLUMNS * BOX_SIZE
height = (ROWS+1) * BOX_SIZE

size = (width, height)

RADIUS = int(BOX_SIZE/2 - 10)

screen = pg.display.set_mode(size)
draw_game_board(game_board)
pg.display.update()

myfont = pg.font.SysFont("Times New Roman", 75)

turn = random.randint(PLAYER, AI)

while not game_ends:

	for event in pg.event.get():
		if event.type == pg.QUIT:
			sys.exit()

		if event.type == pg.MOUSEMOTION:
			pg.draw.rect(screen, BLACK, (0,0, width, BOX_SIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pg.draw.circle(screen, RED, (posx, int(BOX_SIZE/2)), RADIUS)

		pg.display.update()

		if event.type == pg.MOUSEBUTTONDOWN:
			pg.draw.rect(screen, BLACK, (0,0, width, BOX_SIZE))
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/BOX_SIZE))

				if is_valid_move(game_board, col):
					row = get_row_location(game_board, col)
					set_piece(game_board, row, col, PLAYER_PIECE)

					if winning_move(game_board, PLAYER_PIECE):
						label = myfont.render("You WIN", 1, WHITE)
						screen.blit(label, (300,10))
						game_ends = True

					turn = AI

					draw_game_board(game_board)

	if turn == AI and not game_ends:

		col, minimax_score = minimax(game_board, DIFFICULTY, -INFINITY, INFINITY, True)

		if is_valid_move(game_board, col):
			row = get_row_location(game_board, col)
			set_piece(game_board, row, col, AI_PIECE)

			if winning_move(game_board, AI_PIECE):
				label = myfont.render("YOU LOSE", 1, WHITE)
				screen.blit(label, (300,10))
				game_ends = True

			draw_game_board(game_board)

			turn = PLAYER

	if game_ends:
		pg.time.wait(4000)