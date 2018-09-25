import pygame
import numpy as np
from random import randint
from time import sleep

pygame.init()

class chain_game():
	def __init__(self):
		self.define_game_constants()

	def define_game_constants(self):
		pygame.display.set_caption("My Game")

		self.cell_width, self.cell_height = 40,40
		self.edge_space, self.edge_width = 4,1
		self.no_rows, self.no_cols = 12, 10
		self.display_height, self.display_width = self.no_rows*self.cell_width + 2*self.edge_space, self.no_cols*self.cell_height + 2*self.edge_space
		self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
		self.clock = pygame.time.Clock()

		self.radius, self.vibration = [0,12,10,8], [[0,0,0,0],[0,3,0,0],[0,2,3,0],[0,1,2,3]]
		self.frequency = [[0,0,0,0],[0,100,0,0],[0,50,100,0],[0,25,50,100]]
		self.speed = [[100000,100000,100000,100000],[100000,200,100000,100000],[100000,400,200,100000],[100000,800,400,200]]
		self.high_freq = 1000
		self.high_speed = 100

		self.max_balls = np.zeros((self.no_rows,self.no_cols),dtype=int)
		self.ball_pos_root = np.zeros((self.no_rows,self.no_cols,4,3,2))

		self.mouse_pos = pygame.mouse.get_pos()
		self.mouse_clk = pygame.mouse.get_pressed()

		self.set_grid_vals()
		self.define_colors()

	def set_grid_vals(self):
		self.max_balls[0][0], self.max_balls[self.no_rows-1][0], self.max_balls[0][self.no_cols-1], self.max_balls[self.no_rows-1][self.no_cols-1] = 1, 1, 1, 1
		self.max_balls[0,1:self.no_cols-1], self.max_balls[self.no_rows-1,1:self.no_cols-1],self.max_balls[1:self.no_rows-1,0], self.max_balls[1:self.no_rows-1,self.no_cols-1] = 2, 2, 2, 2
		self.max_balls[1:self.no_rows-1,1:self.no_cols-1] = 3
		print(self.max_balls)
		for i in range(self.no_rows):
			for j in range(self.no_cols):
				x, y = int(self.edge_space + self.cell_width*(0.5+j)), int(self.edge_space + self.cell_height*(0.5+i))
				self.ball_pos_root[i][j][1][0][0], self.ball_pos_root[i][j][1][0][1] = x, y

				x, y = int(self.edge_space + self.cell_width*(0.3+j)), int(self.edge_space + self.cell_height*(0.5+i))
				self.ball_pos_root[i][j][2][0][0], self.ball_pos_root[i][j][2][0][1] = x, y
				x, y = int(self.edge_space + self.cell_width*(0.7+j)), int(self.edge_space + self.cell_height*(0.5+i))
				self.ball_pos_root[i][j][2][1][0], self.ball_pos_root[i][j][2][1][1] = x, y

				x, y = int(self.edge_space + self.cell_width*(0.3+j)), int(self.edge_space + self.cell_height*(0.65+i))
				self.ball_pos_root[i][j][3][0][0], self.ball_pos_root[i][j][3][0][1] = x, y
				x, y = int(self.edge_space + self.cell_width*(0.7+j)), int(self.edge_space + self.cell_height*(0.65+i))
				self.ball_pos_root[i][j][3][1][0], self.ball_pos_root[i][j][3][1][1] = x, y
				x, y = int(self.edge_space + self.cell_width*(0.5+j)), int(self.edge_space + self.cell_height*(0.25+i))
				self.ball_pos_root[i][j][3][2][0], self.ball_pos_root[i][j][3][2][1] = x, y

	def define_colors(self):
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.red = (255,0,0)
		self.green = (0,255,0)
		self.blue = (0,0,255)
		self.l_red = (170,0,0)
		self.l_green = (0,170,0)
		self.l_blue = (0,0,170)

	def define_play_variables(self):
		self.player_color = {0:self.black, 1:self.red,2:self.blue,3:self.green}
		self.player_names = {0:"self.black", 1:"red player",2:"blue player ",3:"green player "}
		self.now_player, self.tot_players = 2, 3 

		self.grid_player = np.zeros((self.no_rows,self.no_cols),dtype=int)
		self.grid_balls = np.zeros((self.no_rows,self.no_cols),dtype=int)
		self.ball_pos = np.zeros((self.no_rows,self.no_cols,4,3,2))
		self.ball_pos = self.ball_pos_root.copy()

		self.players_alive = np.ones(self.tot_players+1)
		self.players_alive[0] = 0
		self.round_one = self.tot_players
		self.my_clock = 1

		self.game_over = False

	def play(self):
		self.define_play_variables()
		self.game_loop()

	def game_loop(self):
		self.update_display()
		while not self.game_over:
			self.mouse_pos = pygame.mouse.get_pos()
			self.mouse_clk = pygame.mouse.get_pressed()
			sleep(0.00075)
			if(self.my_clock%self.high_speed == 0):
				for i in range(self.no_rows):
					for j in range(self.no_cols):
						if(self.my_clock%self.speed[self.max_balls[i][j]][self.grid_balls[i][j]]):
							for k in range(self.grid_balls[i][j]):
								vibrate = self.vibration[self.max_balls[i][j]][self.grid_balls[i][j]]
								self.ball_pos[i][j][self.grid_balls[i][j]][k][0] = self.ball_pos_root[i][j][self.grid_balls[i][j]][k][0] + randint(-vibrate,vibrate)
								self.ball_pos[i][j][self.grid_balls[i][j]][k][1] = self.ball_pos_root[i][j][self.grid_balls[i][j]][k][1] + randint(-vibrate,vibrate)
								# self.draw_circle(i,j,self.player_color[self.grid_player[i][j]])
				self.update_display()
				pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.game_over = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						self.game_over = True

			self.my_clock += 1
			if(self.my_clock%32001 == 0):
				self.my_clock = 1
			if(self.round_one==0):
				self.game_over = not(self.game_active())

	def update_display(self):
		self.mouse_pos = pygame.mouse.get_pos()
		self.mouse_clk = pygame.mouse.get_pressed()	
		self.draw_grid(self.player_color[self.now_player])
		self.make_btns()

	def make_btns(self):
		for i in range(self.no_rows):
			for j in range(self.no_cols):
				color = self.player_color[self.grid_player[i][j]]
				self.draw_circle(i,j,color)

	def game_active(self):
		actives = 0
		for i in range(self.tot_players):
			if(self.player_alive(i)):
				actives += 1
		if(actives>1):
			return True
		else:
			return False

	def player_alive(self,ply_no):
		for i in range(self.no_rows):
			for j in range(self.no_cols):
				if(self.grid_player[i][j]==ply_no):
					return True
		return False

	def draw_grid(self,color):
		self.gameDisplay.fill(self.black)
		for i in range(self.edge_space,self.display_width,self.cell_width):
			pygame.draw.line(self.gameDisplay, color, (i,self.edge_space),(i,self.display_height-self.edge_space),self.edge_width)
		for i in range(self.edge_space,self.display_height,self.cell_height):
			pygame.draw.line(self.gameDisplay, color, (self.edge_space,i),(self.display_width-self.edge_space,i),self.edge_width)

	def draw_circle(self,row,col,color):
		if(self.edge_space + self.cell_width*(col)<self.mouse_pos[0]<self.edge_space + self.cell_width*(1+col)):
			if(self.mouse_clk[0]==1):
				if(self.edge_space + self.cell_height*(row)<self.mouse_pos[1]<self.edge_space + self.cell_height*(1+row)):
					self.cell_clicked(row,col)
					print("clicked")
		for k in range(self.grid_balls[row][col]):
			x, y = int(self.ball_pos[row][col][self.grid_balls[row][col]][k][0]), int(self.ball_pos[row][col][self.grid_balls[row][col]][k][1])
			pygame.draw.circle(self.gameDisplay, color , (x,y),self.radius[self.grid_balls[row][col]])

	def cell_clicked(self,row,col):
		if(self.now_player == self.grid_player[row][col] or 0 == self.grid_player[row][col]):
			self.grid_balls[row][col] +=1
			self.grid_player[row][col] = self.now_player
			self.upgrade_grid(row,col)
			x = self.now_player
			x = ((x)%self.tot_players)+1
			if(self.round_one==0):
				can_play = False
				while not can_play:
					if(self.player_alive(x)):
						can_play = True
					else:
						x = ((x)%self.tot_players)+1
						self.players_alive[x] = 0
					if(np.sum(self.players_alive)==1):
						x = self.now_player
						can_play = True
			else:
				self.round_one -= 1
			self.now_player = x

	def upgrade_grid(self,row,col):
		if(row==0 and col==0):
			if(self.grid_balls[row][col]==2):
				self.grid_balls[row][col] = 0 
				self.grid_player[row][col] = 0
				self.add_ball(row+1,col)
				self.add_ball(row,col+1)
		elif(row==0 and col==self.no_cols-1):
			if(self.grid_balls[row][self.no_cols-1]==2):
				self.grid_balls[row][self.no_cols-1] = 0 
				self.grid_player[row][col] = 0
				self.add_ball(row+1,self.no_cols-1)
				self.add_ball(row,self.no_cols-2)
		elif(row==self.no_rows-1 and col==0):
			if(self.grid_balls[row][col]==2):
				self.grid_balls[row][col] = 0 
				self.grid_player[row][col] = 0
				self.add_ball(row-1,0)
				self.add_ball(row,1)
		elif(row==self.no_rows-1 and col==self.no_cols-1):
			if(self.grid_balls[row][col]==2):
				self.grid_balls[row][col] = 0 
				self.grid_player[row][col] = 0
				self.add_ball(row-1,col)
				self.add_ball(row,col-1)
		elif(row==0):
			if(self.grid_balls[row][col]==3):
				self.grid_balls[row][col] = 0 
				self.grid_player[row][col] = 0
				self.add_ball(row,col+1)
				self.add_ball(row+1,col)
				self.add_ball(row,col-1)
		elif(col==self.no_cols-1):
			if(self.grid_balls[row][col]==3):
				self.grid_balls[row][col] = 0 
				self.grid_player[row][col] = 0
				self.add_ball(row-1,col)
				self.add_ball(row+1,col)
				self.add_ball(row,col-1)
		elif(row==self.no_rows-1):
			if(self.grid_balls[row][col]==3):
				self.grid_balls[row][col] = 0 
				self.grid_player[row][col] = 0
				self.add_ball(row-1,col)
				self.add_ball(row,col+1)
				self.add_ball(row,col-1)
		elif(col==0):
			if(self.grid_balls[row][col]==3):
				self.grid_balls[row][col] = 0 
				self.grid_player[row][col] = 0
				self.add_ball(row-1,col)
				self.add_ball(row,col+1)
				self.add_ball(row+1,col)
		else:
			if(self.grid_balls[row][col]==4):
				self.grid_balls[row][col] = 0 
				self.grid_player[row][col] = 0
				self.add_ball(row-1,col)
				self.add_ball(row,col+1)
				self.add_ball(row+1,col)
				self.add_ball(row,col-1)

	def add_ball(self,row,col):
		self.grid_balls[row][col] += 1
		self.grid_player[row][col] = self.now_player
		self.upgrade_grid(row,col)

game = chain_game()
game.play()

