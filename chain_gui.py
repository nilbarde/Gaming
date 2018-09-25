import pygame
import numpy as np
from random import randint
from time import sleep

pygame.init()

class chain_game():
	def __init__(self):
		self.cell_width, self.cell_height = 40,40
		self.edge_space, self.edge_width = 4,1
		self.no_rows, self.no_cols = 12, 10
		self.radius, self.vibrate, self.update_after_iters = [0,12,10,8], [0,2,1,1], 1000
		self.display_height, self.display_width = self.no_rows*self.cell_width + 2*self.edge_space, self.no_cols*self.cell_height + 2*self.edge_space
		self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
		self.mouse_pos = pygame.mouse.get_pos()
		self.mouse_clk = pygame.mouse.get_pressed()

		self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
		pygame.display.set_caption("My Game")
		self.clock = pygame.time.Clock()
		self.define_colors()
		self.player_color = {0:self.black, 1:self.red,2:self.blue,3:self.green}
		self.player_names = {0:"self.black", 1:"red player",2:"blue player ",3:"green player "}
		self.now_player, self.tot_players = 2, 3 
		self.play_game()
		print(self.grid_player)
		sleep(30)

	def message_display(self,text):
		largetext = pygame.font.Font("freesansbold.ttf",30)
		textsurf, textrect = self.text_objs(text,largetext)
		textrect.center = ((self.display_width/2),(self.display_height/2))
		self.gameDisplay.blit(textsurf,textrect)
		pygame.display.update()

	def text_objs(self,text,font):
		textsurf = font.render(text, True, self.white)
		return textsurf, textsurf.get_rect()

	def play_game(self):
		self.grid_player = np.zeros((self.no_rows,self.no_cols),dtype=int)
		self.grid_balls = np.zeros((self.no_rows,self.no_cols),dtype=int)
		self.ball_pos = np.zeros((self.no_rows,self.no_cols,3,2,2))

		self.players_alive = np.ones(self.tot_players+1)
		self.players_alive[0] = 0
		self.round_one = self.tot_players

		print("running")
		self.make_btns()
		self.play_true = True
		self.vibrate_timer = 1
		while(np.sum(self.players_alive)>1):
			sleep(0.00001)
			self.vibrate_timer+=1
			self.mouse_pos = pygame.mouse.get_pos()
			self.mouse_clk = pygame.mouse.get_pressed()
			if(self.vibrate_timer == self.update_after_iters):
				self.draw_grid(self.player_color[self.now_player])
				for i in range(self.no_rows):
					for j in range(self.no_cols):
						color = self.player_color[self.grid_player[i][j]]
						self.draw_circle(i,j,color)

				# self.update_display()
			if(self.vibrate_timer==1000)
				self.vibrate_timer = 1
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.play_true = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						self.play_true = False
		self.make_btns()
		self.update_display()
		self.winner_text = self.player_names[self.now_player] + 'won the game'
		self.message_display(self.winner_text)

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
		pygame.display.update()

	def define_colors(self):
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.red = (255,0,0)
		self.green = (0,255,0)
		self.blue = (0,0,255)
		self.l_red = (170,0,0)
		self.l_green = (0,170,0)
		self.l_blue = (0,0,170)

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

	def player_alive(self,ply_no):
		for i in range(self.no_rows):
			for j in range(self.no_cols):
				if(self.grid_player[i][j]==ply_no):
					return True
		return False
	def draw_circle(self,row,col,color=None):
		if(self.edge_space + self.cell_width*(col)<self.mouse_pos[0]<self.edge_space + self.cell_width*(1+col)):
			if(self.mouse_clk[0]==1):
				if(self.edge_space + self.cell_height*(row)<self.mouse_pos[1]<self.edge_space + self.cell_height*(1+row)):
					self.cell_clicked(row,col)
					print("clicked")
					# self.grid_balls[row][col] += 1

		if(self.grid_balls[row][col]==1):
			x = int(self.edge_space + self.cell_width*(0.5+col)) + randint(-self.vibrate[1],self.vibrate[1])
			y = int(self.edge_space + self.cell_height*(0.5+row)) + randint(-self.vibrate[1],self.vibrate[1])
			pygame.draw.circle(self.gameDisplay, color , (x,y),self.radius[1])

		if(self.grid_balls[row][col]==2):
			x = int(self.edge_space + self.cell_width*(0.3+col)) + randint(-self.vibrate[2],self.vibrate[2])
			y = int(self.edge_space + self.cell_height*(0.5+row)) + randint(-self.vibrate[2],self.vibrate[2])
			pygame.draw.circle(self.gameDisplay, color , (x,y),self.radius[2])
			x = int(self.edge_space + self.cell_width*(0.7+col)) + randint(-self.vibrate[2],self.vibrate[2])
			y = int(self.edge_space + self.cell_height*(0.5+row)) + randint(-self.vibrate[2],self.vibrate[2])
			pygame.draw.circle(self.gameDisplay, color , (x,y),self.radius[2])

		if(self.grid_balls[row][col]==3):
			x = int(self.edge_space + self.cell_width*(0.3+col)) + randint(-self.vibrate[3],self.vibrate[3])
			y = int(self.edge_space + self.cell_height*(0.65+row)) + randint(-self.vibrate[3],self.vibrate[3])
			pygame.draw.circle(self.gameDisplay, color , (x,y),self.radius[3])
			x = int(self.edge_space + self.cell_width*(0.7+col)) + randint(-self.vibrate[3],self.vibrate[3])
			y = int(self.edge_space + self.cell_height*(0.65+row)) + randint(-self.vibrate[3],self.vibrate[3])
			pygame.draw.circle(self.gameDisplay, color , (x,y),self.radius[3])
			x = int(self.edge_space + self.cell_width*(0.5+col)) + randint(-self.vibrate[3],self.vibrate[3])
			y = int(self.edge_space + self.cell_height*(0.25+row)) + randint(-self.vibrate[3],self.vibrate[3])
			pygame.draw.circle(self.gameDisplay, color , (x,y),self.radius[3])
		# pygame.display.update()

	def draw_grid(self,color):
		self.gameDisplay.fill(self.black)
		for i in range(self.edge_space,self.display_width,self.cell_width):
			pygame.draw.line(self.gameDisplay, color, (i,self.edge_space),(i,self.display_height-self.edge_space),self.edge_width)
		for i in range(self.edge_space,self.display_height,self.cell_height):
			pygame.draw.line(self.gameDisplay, color, (self.edge_space,i),(self.display_width-self.edge_space,i),self.edge_width)
		# pygame.display.update()

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




