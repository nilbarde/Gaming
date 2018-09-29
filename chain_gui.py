import pygame
import numpy as np
from random import randint
from time import sleep
from functools import partial 

pygame.init()

class chain_game():
	def __init__(self):
		self.define_game_constants()

	def define_game_constants(self):
		pygame.display.set_caption("My Game")

		self.edge_space, self.edge_width, self.button_height = 4, 1, 0
		self.grid_height, self.grid_width = 480,400
		self.display_height, self.display_width = self.grid_height + 2*self.edge_space + self.button_height, self.grid_width + 2*self.edge_space
		self.no_rows, self.no_cols = 6, 4
		self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
		self.clock = pygame.time.Clock()

		self.frequency = [[0,0,0,0],[0,100,0,0],[0,50,100,0],[0,25,50,100]]
		self.speed = [[100000,100000,100000,100000,100000],[100000,200,100000,100000,100000],[100000,400,200,100000,100000],[100000,800,400,200,10000,10000]]
		self.high_freq = 1000
		self.high_speed = 100
		self.move_steps = 40.0
		self.transition_time = 0.25
		self.player_color_pos = [
								[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],
								[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],
								[[0,0],[0.5,0.5],[0.64,0.5],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],
								[[0,0],[0.46,0.5],[0.575,0.5],[0.69,.5],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],
								[[0,0],[0.425,0.5],[0.525,0.5],[0.625,0.5],[0.725,0.5],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],
								[[0,0],[0.415,0.5],[0.495,0.5],[0.575,0.5],[0.655,0.5],[0.735,0.5],[0,0],[0,0],[0,0],[0,0],[0,0]],
								[[0,0],[0.46,0.25],[0.46,0.75],[0.575,0.25],[0.575,0.75],[0.69,.25],[0.69,.75],[0,0],[0,0],[0,0],[0,0]],
								[[0,0],[0.425,0.25],[0.425,0.75],[0.525,0.25],[0.525,0.75],[0.625,0.25],[0.625,0.75],[0.725,0.5],[0,0],[0,0],[0,0]],
								[[0,0],[0.425,0.25],[0.425,0.75],[0.525,0.25],[0.525,0.75],[0.625,0.25],[0.625,0.75],[0.725,0.25],[0.725,0.75],[0,0],[0,0]],
								[[0,0],[0.415,0.25],[0.415,0.75],[0.495,0.25],[0.495,0.75],[0.575,0.25],[0.575,0.75],[0.655,0.25],[0.655,0.75],[0.735,0.5],[0,0]],
								[[0,0],[0.415,0.25],[0.415,0.75],[0.495,0.25],[0.495,0.75],[0.575,0.25],[0.575,0.75],[0.655,0.25],[0.655,0.75],[0.735,0.25],[0.735,0.75]]
								]

		self.mouse_pos = pygame.mouse.get_pos()
		self.mouse_clk = pygame.mouse.get_pressed()

		self.define_colors()
		self.player_color = {}
		self.player_color_id = {}
		self.player_color[0] = self.black
		for i in range(10):
			self.player_color[i+1] = self.all_colors[i]
			self.player_color_id[i+1] = i
		
		self.define_play_variables()
		self.mode = "moving"
		pygame.display.update()


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

				x, y = int(self.edge_space + self.cell_width*(0.25+j)), int(self.edge_space + self.cell_height*(0.25+i))
				self.ball_pos_root[i][j][4][0][0], self.ball_pos_root[i][j][4][0][1] = x, y
				x, y = int(self.edge_space + self.cell_width*(0.25+j)), int(self.edge_space + self.cell_height*(0.75+i))
				self.ball_pos_root[i][j][4][1][0], self.ball_pos_root[i][j][4][1][1] = x, y
				x, y = int(self.edge_space + self.cell_width*(0.75+j)), int(self.edge_space + self.cell_height*(0.25+i))
				self.ball_pos_root[i][j][4][2][0], self.ball_pos_root[i][j][4][2][1] = x, y
				x, y = int(self.edge_space + self.cell_width*(0.75+j)), int(self.edge_space + self.cell_height*(0.75+i))
				self.ball_pos_root[i][j][4][3][0], self.ball_pos_root[i][j][4][3][1] = x, y

				x, y = int(self.edge_space + self.cell_width*(0.5+j)), int(self.edge_space + self.cell_height*(0.5+i))
				self.ball_pos_root[i][j][5][0][0], self.ball_pos_root[i][j][5][0][1] = x, y
				self.ball_pos_root[i][j][5][1][0], self.ball_pos_root[i][j][5][1][1] = x, y
				self.ball_pos_root[i][j][5][2][0], self.ball_pos_root[i][j][5][2][1] = x, y
				self.ball_pos_root[i][j][5][3][0], self.ball_pos_root[i][j][5][3][1] = x, y
				self.ball_pos_root[i][j][5][4][0], self.ball_pos_root[i][j][5][4][1] = x, y

	def define_colors(self):
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.dark_red = (255,0,0)
		self.dark_green = (0,255,0)
		self.dark_blue = (0,0,255)
		self.red = (170,0,0)
		self.green = (0,170,0)
		self.blue = (0,0,170)
		self.dark_gray = (50,50,50)
		self.gray = (150,150,150)
		self.aqua = (0,255,255)
		self.magenta = (255,0,255)
		self.olive = (128,128,0)
		self.purple = (128,0,128)
		self.teal = (0,128,128)
		self.orange = ((255,140,0))
		self.all_colors = [self.red,self.green,self.blue,self.gray,self.aqua,self.magenta,self.olive,self.purple,self.teal,self.orange]

	def define_play_variables(self):
		self.cell_width, self.cell_height = self.grid_width/self.no_cols, self.grid_height/self.no_rows
		print(self.cell_height,self.cell_width)

		self.max_balls = np.zeros((self.no_rows,self.no_cols),dtype=int)
		self.ball_pos_root = np.zeros((self.no_rows,self.no_cols,6,5,2))
		self.set_grid_vals()

		self.root_radi = min(self.cell_width,self.cell_height)/3.33
		print(self.root_radi)
		self.radius, self.vibration = [0,int(self.root_radi),int(self.root_radi*0.84),int(self.root_radi*0.7),int(self.root_radi*0.5),int(self.root_radi)], [[0,0,0,0,0,0],[0,3,0,0,0,0],[0,2,3,0,0,0],[0,1,2,3,0,0],[0,1,2,3,4,0],[0,1,2,3,4,5]]

		self.player_names = {0:"self.black", 1:"red player",2:"blue player ",3:"green player "}
		self.now_player, self.tot_players = 1, 2

		self.grid_player = np.zeros((self.no_rows,self.no_cols),dtype=int)
		self.grid_balls = np.zeros((self.no_rows,self.no_cols),dtype=int)
		self.ball_pos = np.zeros((self.no_rows,self.no_cols,6,5,2))
		self.ball_pos = self.ball_pos_root.copy()

		self.players_alive = np.ones(self.tot_players+1)
		self.players_alive[0] = 0
		self.round_one = self.tot_players
		self.my_clock = 1

		self.game_over = False
		self.option_over = False
		self.after_game_option = False

	def play(self):
		self.define_play_variables()
		self.game_loop()
		self.mode = "moving"
		self.update_display()
		winner_text = "player " + str(self.now_player) + " won the game"
		self.message_display(winner_text,self.display_width/2,self.display_height*0.3,30,self.player_color[self.now_player])
		pygame.display.update()
		self.after_game_option = False
		while not self.after_game_option:
			for event in pygame.event.get():
				self.mouse_pos = pygame.mouse.get_pos()
				self.mouse_clk = pygame.mouse.get_pressed()
			self.add_button(self.play,"Play Again",self.display_width/2,self.display_height*0.45,self.display_width*0.4,self.display_height*0.1,self.dark_green,self.green,self.black)
			self.add_button(self.option_window,"Reset",self.display_width/2,self.display_height*0.6,self.display_width*0.4,self.display_height*0.1,self.dark_green,self.green,self.black)
			self.add_button(self.home_loop,"Home",self.display_width/2,self.display_height*0.75,self.display_width*0.4,self.display_height*0.1,self.dark_green,self.green,self.black)
			self.add_button(self.game_quit,"Quit",self.display_width/2,self.display_height*0.90,self.display_width*0.4,self.display_height*0.1,self.dark_red,self.red,self.black)
			pygame.display.update()

		sleep(4)

	def home_loop(self):
		print("here")
		sleep(0.2)
		print("hhhhhhhhhh")
		while True:
			self.gameDisplay.fill(self.black)
			print(self.mouse_pos)
			for event in pygame.event.get():
				self.mouse_pos = pygame.mouse.get_pos()
				self.mouse_clk = pygame.mouse.get_pressed()
			self.message_display("New Game",self.display_width/2,self.display_height*0.3,40,self.white)
			self.add_button(self.option_window,"Play",self.display_width/2,self.display_height*0.6,self.display_width*0.4,self.display_height*0.15,self.dark_green,self.green,self.black)
			self.add_button(self.game_quit,"Quit",self.display_width/2,self.display_height*0.8,self.display_width*0.4,self.display_height*0.15,self.dark_red,self.red,self.black)
			pygame.display.update()

	def option_window(self):
		sleep(0.1)
		# self.gameDisplay.fill(self.black)
		self.option_over = False
		while not self.option_over:
			self.gameDisplay.fill(self.black)
			sleep(0.09)
			for event in pygame.event.get():
				self.mouse_pos = pygame.mouse.get_pos()
				self.mouse_clk = pygame.mouse.get_pressed()
			# (self,action,text,center_x,center_y,width,height,on_color,off_color,text_color)
			self.show_selected()
			self.add_button(self.play,"Start",self.display_width*0.5,self.display_height*0.85,self.display_width*0.4,self.display_height*0.075,self.dark_green,self.green,self.black)
			self.add_button(self.home_loop,"Goo Back",self.display_width*0.5,self.display_height*0.95,self.display_width*0.4,self.display_height*0.075,self.dark_red,self.red,self.black)

			pygame.display.update()

	def show_selected(self):
		self.message_display("Players",self.display_width*0.5,self.display_height*0.2,40,self.white)
		self.message_display(str(self.tot_players),self.display_width*0.5,self.display_height*0.3,40,self.white)
		self.add_button(partial(self.add_val,1,'player'),"+",self.display_width*0.6,self.display_height*0.3,self.display_width*0.1,self.display_height*0.1,self.dark_gray,self.gray,self.black)
		self.add_button(partial(self.add_val,-1,'player'),"-",self.display_width*0.4,self.display_height*0.3,self.display_width*0.1,self.display_height*0.1,self.dark_gray,self.gray,self.black)

		self.message_display("Rows",self.display_width*0.25,self.display_height*0.05,40,self.white)
		self.message_display(str(self.no_rows),self.display_width*0.25,self.display_height*0.1,40,self.white)
		self.add_button(partial(self.add_val,1,"row"),"+",self.display_width*0.35,self.display_height*0.1,self.display_width*0.075,self.display_height*0.075,self.dark_gray,self.gray,self.black)
		self.add_button(partial(self.add_val,-1,"row"),"-",self.display_width*0.15,self.display_height*0.1,self.display_width*0.075,self.display_height*0.075,self.dark_gray,self.gray,self.black)
		self.message_display("Columns",self.display_width*0.75,self.display_height*0.05,40,self.white)
		self.message_display(str(self.no_cols),self.display_width*0.75,self.display_height*0.1,40,self.white)
		self.add_button(partial(self.add_val,1,"col"),"+",self.display_width*0.85,self.display_height*0.1,self.display_width*0.075,self.display_height*0.075,self.dark_gray,self.gray,self.black)
		self.add_button(partial(self.add_val,-1,"col"),"-",self.display_width*0.65,self.display_height*0.1,self.display_width*0.075,self.display_height*0.075,self.dark_gray,self.gray,self.black)

		for i in range(1,self.tot_players+1):
			self.add_button(None," ",(self.player_color_pos[self.tot_players][i][1])*self.display_width ,(self.player_color_pos[self.tot_players][i][0])*self.display_height ,self.display_width*0.06,self.display_height*0.06,self.player_color[i],self.player_color[i],self.black)
			self.add_button(partial(self.add_val,(i),"color"),"->",(self.player_color_pos[self.tot_players][i][1]+0.1)*self.display_width ,(self.player_color_pos[self.tot_players][i][0])*self.display_height ,self.display_width*0.06,self.display_height*0.06,self.gray,self.gray,self.black)
			self.add_button(partial(self.add_val,-(i),"color"),"<-",(self.player_color_pos[self.tot_players][i][1]-0.1)*self.display_width ,(self.player_color_pos[self.tot_players][i][0])*self.display_height ,self.display_width*0.06,self.display_height*0.06,self.gray,self.gray,self.black)

	def option_tog(self):
		self.option_over = not self.option_over

	def add_val(self,how_many,what):
		if(what=="player"):
			self.tot_players += how_many
			if(self.tot_players<2):
				self.tot_players = 2
			elif(self.tot_players>10):
				self.tot_players = 10
		elif(what=="row"):
			self.no_rows += how_many
			if(self.no_rows<2):
				self.no_rows = 2
		elif(what=="col"):
			self.no_cols += how_many
			if(self.no_cols<2):
				self.no_cols = 2
		elif(what=="color"):
			if(how_many>0):
				self.player_color_id[how_many] = (self.player_color_id[how_many]+1)%10
				self.player_color[how_many] = self.all_colors[(self.player_color_id[how_many])]
			elif(how_many<0):
				self.player_color_id[-(how_many)] = (self.player_color_id[-(how_many)]-1)%10
				self.player_color[-(how_many)] = self.all_colors[(self.player_color_id[-(how_many)]-1)]

	def game_loop(self):
		print(self.grid_balls)
		print(self.tot_players)
		print(self.player_color_id)
		print(self.player_color)
		self.update_display()
		self.mode = "not moving"
		sleep(0.15)
		self.mouse_pos = pygame.mouse.get_pos()
		self.mouse_clk = pygame.mouse.get_pressed()
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

			self.my_clock += 1
			if(self.my_clock%32001 == 0):
				self.my_clock = 1
			if(self.round_one==0):
				self.game_over = not(self.game_active())

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.game_over = True
					self.game_quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						self.game_over = True
						self.game_quit()
		self.mode = "moving"

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
		print(self.grid_player[0][0],self.player_color[0])

	def game_active(self):
		actives = 0
		for i in range(1,self.tot_players+1):
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
		for i in range(self.edge_space,(self.edge_space+self.grid_width+1),self.cell_width):
			pygame.draw.line(self.gameDisplay, color, (i,self.edge_space),(i,(self.edge_space+(self.no_rows)*self.cell_height)),self.edge_width)
		for i in range(self.edge_space,(self.edge_space+self.grid_height+1),self.cell_height):
			pygame.draw.line(self.gameDisplay, color, (self.edge_space,i),((self.edge_space+(self.no_cols)*self.cell_width),i),self.edge_width)
		self.mouse_pos = pygame.mouse.get_pos()
		self.mouse_clk = pygame.mouse.get_pressed()
		if(self.mode!="moving"):
			if((self.display_width/2<self.mouse_pos[0]<self.display_width) and (self.display_height-self.button_height<self.mouse_pos[0]<self.display_height)):
				if(self.mouse_clk[0]==1):
					self.game_over = True
					print("exit")
					self.game_quit()
		pygame.draw.rect(self.gameDisplay, self.dark_red, (self.display_width/2,self.display_height-self.button_height,self.display_width,self.display_height))

	def draw_circle(self,row,col,color):
		if(self.mode!="moving"):
			if(self.edge_space + self.cell_width*(col)<self.mouse_pos[0]<self.edge_space + self.cell_width*(1+col)):
				if(self.mouse_clk[0]==1):
					if(self.edge_space + self.cell_height*(row)<self.mouse_pos[1]<self.edge_space + self.cell_height*(1+row)):
						self.cell_clicked(row,col)
						print("clicked")
		for k in range(self.grid_balls[row][col]):
			x, y = int(self.ball_pos[row][col][self.grid_balls[row][col]][k][0]), int(self.ball_pos[row][col][self.grid_balls[row][col]][k][1])
			pygame.draw.circle(self.gameDisplay, color , (x,y),self.radius[self.grid_balls[row][col]])

	def move_circle(self,x_1,y_1,x_2,y_2,color):
		x01 = np.array(x_1)
		x02 = np.array(x_2)
		y01 = np.array(y_1)
		y02 = np.array(y_2)
		x1,y1,x2,y2 = x_1,y_1,x_2,y_2
		for i in range(len(x01)):
			x1[i] = int(self.edge_space + self.cell_width*(0.5+x01[i]))
			x2[i] = int(self.edge_space + self.cell_width*(0.5+x02[i]))
			y1[i] = int(self.edge_space + self.cell_height*(0.5+y01[i]))
			y2[i] = int(self.edge_space + self.cell_height*(0.5+y02[i]))
		for i in range(int(self.move_steps)):
			# self.draw_grid(color)
			self.update_display()
			for j in range(len(x1)):
				x = int(x1[j] + ((i+1)*(x2[j]-x1[j])/self.move_steps))
				y = int(y1[j] + ((i+1)*(y2[j]-y1[j])/self.move_steps))
				pygame.draw.circle(self.gameDisplay, color , (x,y),self.radius[1])
			pygame.display.update()
			sleep(self.transition_time/self.move_steps)
		for i in range(len(x02)):
			self.grid_balls[y02[i]][x02[i]] += 1
			self.grid_player[y02[i]][x02[i]] = self.now_player

	def cell_clicked(self,row,col):
		if(self.now_player == self.grid_player[row][col] or 0 == self.grid_player[row][col]):
			print("called me")
			self.grid_balls[row][col] +=1
			self.grid_player[row][col] = self.now_player
			# print(self.grid_balls)
			self.mode = "moving"
			self.upgrade_grid()
			self.mode = "not moving"
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

	def upgrade_grid(self):
		if not self.game_active():
			return
		x1,y1,x2,y2 = [],[],[],[]
		print(self.grid_balls)
		for i in range(self.no_rows):
			for j in range(self.no_cols):
				if(self.grid_balls[i][j]>=self.max_balls[i][j]+1):
					# self.grid_balls[i][j] = 0
					# self.grid_player[i][j] = 0
					if(j>0):
						self.grid_balls[i][j] -= 1
						y1.append(i)
						x1.append(j)
						y2.append(i)
						x2.append(j-1)
					if(i<self.no_rows-1):
						self.grid_balls[i][j] -= 1
						y1.append(i)
						x1.append(j)
						y2.append(i+1)
						x2.append(j)
					if(j<self.no_cols-1):
						self.grid_balls[i][j] -= 1
						y1.append(i)
						x1.append(j)
						y2.append(i)
						x2.append(j+1)
					if(i>0):
						self.grid_balls[i][j] -= 1
						y1.append(i)
						x1.append(j)
						y2.append(i-1)
						x2.append(j)
					if(self.grid_balls[i][j]>0):
						self.grid_balls[i][j] -= 1
						y1.append(i)
						x1.append(j)
						y2.append(i)
						x2.append(j)
					else:
						self.grid_player[i][j] = 0
		if(len(x1)>0):
			self.move_circle(x1,y1,x2,y2,self.player_color[self.now_player])
			self.upgrade_grid()
		else:
			return

	def text_objs(sel,text,font,color):
		textsurf = font.render(text, True, color)
		return textsurf, textsurf.get_rect()

	def message_display(self,text,center_x,center_y,text_size=100,color=(0,0,0)):
		try:
			largetext = pygame.font.Font("ARCADE.TTF",text_size)
		except:
			largetext = pygame.font.SysFont("liberationserif",text_size)
		textsurf, textrect = self.text_objs(text,largetext,color)
		textrect.center = ((center_x),(center_y))
		self.gameDisplay.blit(textsurf,textrect)

	def add_button(self,action,text,center_x,center_y,width,height,on_color,off_color,text_color):
		if(center_x+(width/2)>self.mouse_pos[0]>center_x-(width/2) and center_y+(height/2)>self.mouse_pos[1]>center_y-(height/2)):
			pygame.draw.rect(self.gameDisplay, on_color, (center_x-(width/2),center_y-(height/2),width,height))
			if(self.mouse_clk[0]==1 and action != None):
				# print(text,self.mode)
				action()
		else:
			pygame.draw.rect(self.gameDisplay, off_color, (center_x-(width/2),center_y-(height/2),width,height))
		self.message_display(text,center_x,center_y,30,text_color)

	def add_ball(self,row,col):
		self.grid_balls[row][col] += 1
		self.grid_player[row][col] = self.now_player
		self.upgrade_grid(row,col)

	def game_quit(self):
		pygame.quit()
		quit()

game = chain_game()
# game.play()
game.home_loop()
print("sleeping")
sleep(4)
