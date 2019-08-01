import pygame
import numpy as np
from random import randint, shuffle, choice
from time import sleep, time
from functools import partial 
import cv2

pygame.init()

class heli_game():
	def __init__(self):
		self.define_game_constants()
		self.define_colors()

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

	def define_game_constants(self):
		pygame.display.set_caption("My Game")

		self.grid_height, self.grid_width = 500,1000
		self.cell_size = 2
		self.rows, self.cols = self.grid_height//self.cell_size, self.grid_width//self.cell_size
		self.max_border = self.rows//4
		self.display_height, self.display_width = self.rows*self.cell_size, self.cols*self.cell_size
		print(self.display_height, self.display_width)
		self.gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
		self.clock = pygame.time.Clock()
		self.game_grid = np.zeros((2,self.cols),dtype=int)
		self.game_speed = 100.0
		self.init_grid()
		self.heli_height, self.heli_width = self.rows//15, self.cols//15
		self.heli_x, self.heli_y = 2, self.rows//2 - self.heli_height//2
		self.obst_prob = 0.6
		self.obst_probs = [1 for i in range(int(100*self.obst_prob))] + [0 for i in range(int(100*(1-self.obst_prob)))]
		self.obst_height_max = self.rows//4
		self.obst_height_min = self.rows//8
		self.obst_width = self.cols//20
		self.obst_dist_min = self.cols//3
		self.obst_dist_min_limit = self.cols//6
		self.obst_last = self.obst_dist_min
		self.obsts = [[1,22,10]]
		self.level_up_time = (self.obst_dist_min+self.obst_width)*(200/self.game_speed)*self.cell_size
		print(self.level_up_time)
		self.level_time = 0
		self.level = 1
		self.score = 0
		self.cell_occu = np.zeros((self.rows,self.cols),dtype="uint8")
		self.heli_occu = np.zeros((self.rows,self.cols),dtype="uint8")
		# self.heli_img = pygame.image.load("images.jpeg").convert_alpha()
		# pygame.display.set_icon(self.heli_img)
		# self.heli_img = pygame.transform.scale(self.heli_img, (2*self.heli_width, 2*self.heli_height))

		pygame.display.update()

	def init_grid(self):
		last_u = 10
		last_d = 10
		self.change_border = []
		for i in range(5):
			for j in range((5-i)*10):
				self.change_border.append(i)
				self.change_border.append(-i)
		self.game_grid[0,-1] = last_u
		self.game_grid[1,-1] = last_d
		for i in range(self.cols):
			self.update_grid()

	def home_loop(self):
		print("here")
		sleep(0.2)
		print("hhhhhhhhhh")
		while True:
			self.update_display()
			self.gameDisplay.fill(self.black)
			for event in pygame.event.get():
				self.mouse_pos = pygame.mouse.get_pos()
				self.mouse_clk = pygame.mouse.get_pressed()
			self.message_display("New Game",self.display_width/2,self.display_height*0.3,40,self.white)
			self.add_button(self.game_loop,"Play",self.display_width/2,self.display_height*0.6,self.display_width*0.4,self.display_height*0.15,self.dark_green,self.green,self.black)
			self.add_button(self.game_quit,"Quit",self.display_width/2,self.display_height*0.8,self.display_width*0.4,self.display_height*0.15,self.dark_red,self.red,self.black)
			pygame.display.update()

	def game_loop(self):
		self.game_exit = False
		x_s = 0
		y_s = 0
		while not self.game_exit:
			# x_s = 0
			# y_s = 0
			self.update_display()
			self.level_time += 1
			if self.level_time > self.level_up_time:
				self.level_time = 0
				self.game_speed += 5
				self.level += 1
				self.obst_dist_min *= 0.95
				self.obst_dist_min = max(self.obst_dist_min,self.obst_dist_min_limit)
				# self.obst_prob *= 0.95
			sleep(1/self.game_speed)
			y_s = self.get_move()
			print(y_s,"move")
			self.heli_x += x_s
			self.heli_y += y_s
			self.gameDisplay.fill(self.black)
			# self.DrawSnake()
			self.DrawHeli()
			self.GiveObst()
			self.DrawBorder()
			self.IsBroken()
			self.message_display("score = " + str(self.score),self.display_width-100,30,30,self.dark_green)
			self.message_display("level = " + str(self.level) + " (" + str(int((self.level_time*100)//self.level_up_time)) + "%) ",self.display_width-100,self.display_height-30,30,self.dark_green)
			pygame.display.update()

	def update_display(self):
		self.mouse_pos = pygame.mouse.get_pos()
		self.mouse_clk = pygame.mouse.get_pressed()

	def add_button(self,action,text,center_x,center_y,width,height,on_color,off_color,text_color):
		if(center_x+(width/2)>self.mouse_pos[0]>center_x-(width/2) and center_y+(height/2)>self.mouse_pos[1]>center_y-(height/2)):
			pygame.draw.rect(self.gameDisplay, on_color, (center_x-(width/2),center_y-(height/2),width,height))
			if(self.mouse_clk[0]==1 and action != None):
				# print(text,self.mode)
				action()
		else:
			pygame.draw.rect(self.gameDisplay, off_color, (center_x-(width/2),center_y-(height/2),width,height))
		self.message_display(text,center_x,center_y,30,text_color)

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

	def game_quit(self):
		pygame.quit()
		quit()

	def DrawHeli(self):
		self.heli_occu[:,:] = 0
		self.heli_occu[self.heli_y:self.heli_y+self.heli_height,self.heli_x:self.heli_x+self.heli_width] = 1
		pygame.draw.rect(self.gameDisplay,self.red,[self.heli_x*self.cell_size,self.heli_y*self.cell_size,self.heli_width*self.cell_size,self.heli_height*self.cell_size])
		# self.gameDisplay.blit(self.heli_img,(self.heli_x*self.cell_size,self.heli_y*self.cell_size))
		# self.gameDisplay.blit(pygame.transform.flip(self.heli_img, False, False),(0,100))

	def GiveObst(self):
		self.obst_last += 1
		obsts = []
		for x in self.obsts:
			if(x[0]+1<(self.cols+self.obst_width+2)):
				obsts.append([x[0]+1,x[1],x[2]])
			else:
				self.score += 1
		self.obsts = obsts[:]
		if(self.obst_last>=self.obst_width+self.obst_dist_min):
			x = choice(self.obst_probs)
			if x:
				print("new obst")
				self.NewObst()
		self.DrawObsts()

	def NewObst(self):
		obst_height = randint(self.obst_height_min,self.obst_height_max)
		obst_starty = randint(self.max_border,(self.rows-self.max_border-obst_height))
		self.obst_last = 1
		self.obsts.append([1,obst_starty,obst_height])

	def DrawObsts(self):
		# pygame.draw.rect(gameDisplay,color,[center_x-width/2,center_y-height/2,width,height])
		self.cell_occu[:,:] = 0
		for obst in self.obsts:
			self.cell_occu[obst[1]:obst[1]+obst[2],max(self.cols-obst[0],0):self.cols-obst[0]+self.obst_width] = 1
			pygame.draw.rect(self.gameDisplay,self.gray,[self.display_width-(obst[0]*self.cell_size),obst[1]*self.cell_size,self.obst_width*self.cell_size,obst[2]*self.cell_size])

	def DrawBorder(self):
		self.update_grid()
		for i in range(self.cols):
			x = (i + 0.5)*self.cell_size
			self.cell_occu[:self.game_grid[0,i],i] = 1
			self.cell_occu[self.rows-self.game_grid[1,i]:,i] = 1
			# self.cell_occu[self.game_grid[0,i]:self.game_grid[1,i],i] = 0
			pygame.draw.line(self.gameDisplay, self.gray, (x,0),(x,self.game_grid[0,i]*self.cell_size),self.cell_size)
			pygame.draw.line(self.gameDisplay, self.gray, (x,self.display_height-1),(x,self.display_height-(self.game_grid[1,i]*self.cell_size)),self.cell_size)

		# cv2.imwrite("0.png",self.cell_occu*255)

	def update_grid(self):
		last_u = self.game_grid[0,-1]
		last_d = self.game_grid[1,-1]
		self.game_grid[:,:-1] = self.game_grid[:,1:]
		shuffle(self.change_border)
		now_u = last_u + choice(self.change_border)
		now_d = last_d + choice(self.change_border)
		now_u = min(now_u,self.max_border)
		now_u = max(now_u,0)
		now_d = min(now_d,self.max_border)
		now_d = max(now_d,0)
		self.game_grid[0,-1] = now_u
		self.game_grid[1,-1] = now_d

	def IsBroken(self):
		if(np.sum(self.heli_occu*self.cell_occu)):
			print(np.sum(self.heli_occu),np.sum(self.cell_occu))
			print("broken",np.sum(self.heli_occu*self.cell_occu))
			sleep(2)
			self.define_game_constants()
			self.home_loop()

	def message_display(self,text,center_x,center_y,text_size=100,color=(0,0,0)):
		try:
			largetext = pygame.font.Font("ARCADE.TTF",text_size)
		except:
			largetext = pygame.font.SysFont("liberationserif",text_size)
		textsurf, textrect = self.text_objs(text,largetext,color)
		textrect.center = ((center_x),(center_y))
		self.gameDisplay.blit(textsurf,textrect)

	def text_objs(sel,text,font,color):
		textsurf = font.render(text, True, color)
		return textsurf, textsurf.get_rect()

	def get_move(self):
		self.img = self.cell_occu*255
		self.trans = self.get_trans(self.img)
		self.define_dimensions()
		self.get_path()
		return self.path[1]-self.path[0]

	def define_dimensions(self):
		self.img = (self.cell_occu*255).copy()
		self.img_h, self.img_w = self.img.shape
		self.pos_r, self.pos_c = self.heli_y, self.heli_x
		self.my_h,  self.my_w  = self.img_h//15, self.img_w//15
		self.des_r, self.des_c = int(self.img_h//2), (self.img_w//8)-1

	def get_trans(self,img):
		h,w = img.shape
		img = 255 - img
		trans = cv2.distanceTransform(img, cv2.DIST_L2, 5)
		t_max, t_min = (np.amax(trans),np.amin(trans))
		if not t_min==t_max:
			trans = ((trans-t_min)/t_max)*255
		trans = (trans*3).clip(0,255)
		trans = (255 - trans)
		# for i in range(h-self.heli_height):
		# 	for j in range(w-self.heli_width):
		# 		trans[i][j] = np.sum(trans[i:i+self.heli_height,j:j+self.heli_width])/(self.heli_width*self.heli_height)
		trans = trans.astype("uint8")
		return trans

	def get_path(self):
		self.path = self.find_path_forward(self.img,self.trans,self.pos_c,self.pos_r,self.des_c,[+2,-2,+1])
		self.show_path()

	def find_path_forward(self,obst_map,local_map,curr_x,curr_y,des_x,opts):
		img_h, img_w = obst_map.shape
		path_mat = np.zeros((img_h,img_w),dtype=int)
		path_mat.fill(-1)
		path_mat[curr_y,curr_x] = 0
		start_time = time()
		for j in range(curr_x,des_x):
			for i in range(img_h):
				if not path_mat[i,j]==-1:
					for opt in opts:
						if(i+opt<img_h and i+opt>-1):
							if(not(np.sum(obst_map[i+opt:i+opt+self.heli_height,j+1:j+1+self.heli_width]))):
								x = (path_mat[i,j] + local_map[i+opt,j+1])
								y = path_mat[i+opt,j+1]
								if y == -1:
									path_mat[i+opt,j+1] = x
								else:
									path_mat[i+opt,j+1] = min(x,y)
		m = np.amax(path_mat)
		path_mat[path_mat==-1] = m
		path = [curr_y]
		for j in range(curr_x+1,des_x):
			m = np.amax(path_mat[:,j])
			x = -1
			for opt in opts:
				if(path_mat[path[-1]+opt,j]<=m):
					m = path_mat[path[-1]+opt,j]
					x = path[-1]+opt
			path.append(x)
		# print(path)
		# path = [np.argmin(path_mat[:,des_x-1])]
		# for j in range(des_x-2,curr_x-1,-1):
		# 	m = np.amax(path_mat[:,j])
		# 	x = -1
		# 	for opt in opts:
		# 		if(path_mat[path[-1]+opt,j]<=m):
		# 			m = path_mat[path[-1]+opt,j]
		# 			x = path[-1]+opt
		# 	path.append(x)
		# path = path[::-1]
		# path = (np.argmin(path_mat,axis=0))
		end_time = time()
		return path

	def show_path(self):
		self.path_img = self.trans.copy()
		for i in range(self.des_c):
			self.path_img[max(0,self.path[i]-2):min(self.path[i]+3,self.img_h),i] = 128
		# cv2.imwrite("path.png",self.path_img)
		cv2.imshow("path.png",self.path_img)
		cv2.waitKey(1)

game = heli_game()
# game.play()
game.home_loop()

