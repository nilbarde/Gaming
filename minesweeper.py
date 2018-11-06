import kivy

from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.config import Config
from kivy.uix.popup import Popup

from random import shuffle, randint,sample
from functools import partial
import time
import threading

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class Confirmation_Popup(Popup):
	def __init__(self,**kwargs):
		super(Confirmation_Popup,self).__init__(**kwargs)
		self.title = "New Game ???"
		self.layout = GridLayout(cols=2, padding=10, spacing=5)
		self.size_hint = 0.33,0.2
		self.yes_button = Button(text="Yes", on_press=partial(self.set_confirmation,True))
		self.no_button = Button(text="No", on_press=partial(self.set_confirmation,False))
		self.layout.add_widget(self.yes_button)
		self.layout.add_widget(self.no_button)
		self.content = self.layout

	def set_confirmation(self,val,xxx):
		global confirmation, clicked
		confirmation = val
		clicked  = True
		self.dismiss()

class GameScreen(Screen):
	def __init__(self,**kwargs):
		super(GameScreen,self).__init__(**kwargs)
		self.rows = 8
		self.cols = 6
		self.bombs = (self.rows*self.cols)//5
		self.cell_width = 1.0/(self.cols)
		self.cell_height = 0.9/(self.rows)
		self.bomb_width, self.bomb_height = 2*self.cell_width,0.1# 2*self.cell_height
		self.bomb_x, self.bomb_y = self.bomb_width/2, 1.0-(self.bomb_height/2)
		self.new_width, self.new_height = 0.3, 0.08
		self.new_x, self.new_y = 0.5, 0.95
		self.place_bombs = [0 for i in range(self.rows*self.cols)]
		self.grid = [[0 for i in range (self.cols)] for j in range (self.rows)]

	def on_pre_enter(self):
		self.clear_widgets()
		self.decide_bombs()
		btn = Button()
		self.btns = [[btn for i in range(self.cols)]for j in range(self.rows)]
		self.current_btn = "right"
		self.game_over = False
		self.draw_grid()

	def decide_bombs(self):
		just_nums = [i for i in range(len(self.place_bombs))]
		bomb_pos = sample(just_nums,self.bombs)
		self.bombs_remaining = self.bombs
		self.btn_state = [[0 for i in range(self.cols)]for j in range(self.rows)]
		self.grid = [[0 for i in range (self.cols)] for j in range (self.rows)]
		for i in bomb_pos:
			r,c = i//self.cols, i%self.cols
			self.grid[r][c] = -1
		for i in range(self.rows):
			for j in range(self.cols):
				if(self.grid[i][j]!=-1):
					if(i!=(self.rows-1)):
						if(self.grid[i+1][j]==-1):
							self.grid[i][j] += 1
					if(j!=(self.cols-1)):
						if(self.grid[i][j+1]==-1):
							self.grid[i][j] += 1
					if(i!=(0)):
						if(self.grid[i-1][j]==-1):
							self.grid[i][j] += 1
					if(j!=(0)):
						if(self.grid[i][j-1]==-1):
							self.grid[i][j] += 1
					if(i>0 and j>0):
						if(self.grid[i-1][j-1]==-1):
							self.grid[i][j] += 1
					if(i>0 and j<self.cols-1):
						if(self.grid[i-1][j+1]==-1):
							self.grid[i][j] += 1
					if(i<self.rows-1 and j>0):
						if(self.grid[i+1][j-1]==-1):
							self.grid[i][j] += 1
					if(i<self.rows-1 and j<self.cols-1):
						if(self.grid[i+1][j+1]==-1):
							self.grid[i][j] += 1

		for i in range(self.rows):
			for j in range(self.cols):
				print(self.grid[i][j],end=" ")
			print("")

	def draw_grid(self):
		self.bomb_lbl = Button(text=str(self.bombs_remaining),font_size=30,pos_hint={"center_x":self.bomb_x,"center_y":self.bomb_y},size_hint=(self.bomb_width,self.bomb_height))
		self.add_widget(self.bomb_lbl)
		self.new_btn = Button(text="New Game",font_size=30,pos_hint={"center_x":self.new_x,"center_y":self.new_y},size_hint=(self.new_width,self.new_height),on_press=self.new_game_opt)
		self.add_widget(self.new_btn)
		for i in range((self.rows*self.cols)):
			r, c = i//self.cols, i%self.cols
			pos_y = 0.9 - (r+0.5)*self.cell_height
			pos_x = ((c+0.5)*self.cell_width)
			btn = Button(text="",font_size=20,pos_hint={"center_x":pos_x,"center_y":pos_y},size_hint=(self.cell_width,self.cell_height))
			btn.bind(on_touch_down = self.dirPressed)
			btn.bind(state = partial(self.onPressed,r,c))
			self.btns[r][c] = btn
			self.add_widget(self.btns[r][c])

	def dirPressed(self,instance, touch,__="_"):
		if touch.button == 'right':
			# print("right mouse clicked")
			self.current_btn = "right"
		else:
			# print("left")
			self.current_btn = "left"

	def new_game_opt(self,_="_"):
		new_popup = Confirmation_Popup()
		new_popup.open()
		threading.Thread(target=self.go_check).start()

	def go_check(self):
		global confirmation, clicked
		while not(clicked):
			pass
		if(confirmation==True):
			self.on_pre_enter()
		clicked = False

	def onPressed(self,r,c, instance, touch,__="_"):
		if((self.btn_state[r][c] == 0 or self.btn_state[r][c] == 2) and touch == "down" and (not self.game_over)):
			if(self.current_btn=="right"):
				print(self.btn_state[r][c])
				if(self.btn_state[r][c] == 0):
					self.btns[r][c].text = "X"
					self.btn_state[r][c] = 2
					self.bombs_remaining -= 1
					self.btns[r][c].background_color = (0.7,0.7,0.7,1)
					self.bomb_lbl.text=str(self.bombs_remaining)
				elif(self.btn_state[r][c] == 2):
					self.btns[r][c].text = ""
					self.btn_state[r][c] = 0
					self.bombs_remaining += 1
					self.btns[r][c].background_color = (1,1,1,1)
					self.bomb_lbl.text=str(self.bombs_remaining)
			elif(self.current_btn=="left"):
				if(self.grid[r][c]>0):
					self.btns[r][c].text = str(self.grid[r][c])
					self.btns[r][c].background_color = (0.7,0.7,0.7,1)
					if(self.btn_state[r][c] == 2):
						self.bombs_remaining += 1
					self.btn_state[r][c] = 1
				elif(self.grid[r][c]==0):
					self.expand_about(r,c)
					self.btn_state[r][c] = 1
					self.btns[r][c].background_color = (0.7,0.7,0.7,1)
				else:
					self.game_over = True
					self.end_r, self.end_c = r,c
					self.show_answer()
					print("game over")
					self.new_btn.text = "Game Over"
					self.new_btn.font_size = 30
			for r in range(self.rows):
				for c in range(self.cols):
					if not (self.btns[r][c].background_color == (0.7,0.7,0.7,1)):
						return
			self.new_btn.text = "WIN"
			self.new_btn.font_size = 40
		return

	def show_answer(self):
		for r in range(self.rows):
			for c in range(self.cols):
				self.btns[r][c].background_color = (0.7,0.7,0.7,1)				
				if(self.grid[r][c]>0):
					self.btns[r][c].text = str(self.grid[r][c])
				elif(self.grid[r][c]==0):
					self.btns[r][c].text = str("")
				else:
					self.btns[r][c].text = str("X")
					self.btns[r][c].font_size = 30
		self.btns[self.end_r][self.end_c].text = str("X")
		self.btns[self.end_r][self.end_c].font_size = 40

	def expand_about(self,r,c):
		print(r,c)
		for i in range(r-1,r+2):
			if(-1<i<self.rows):
				for j in range(c-1,c+2):
					if(-1<j<self.cols):
						if not(i==r and j==c):
							if not (self.btn_state[i][j]==1):
								if(self.grid[i][j]==0):
									self.btn_state[i][j] = 1
									self.btns[i][j].background_color = (0.7,0.7,0.7,1)
									self.expand_about(i,j)
								else:
									self.btns[i][j].text = str(self.grid[i][j])
									self.btn_state[i][j] = 1
									self.btns[i][j].background_color = (0.7,0.7,0.7,1)

class MainClass(App):
	def build(self):
		ScreenMan = ScreenManagerbuild()

		ScreenMan.add_widget(GameScreen(name='game_window'))		
		return ScreenMan

class ScreenManagerbuild(ScreenManager):
	pass

if __name__ == '__main__':
	global confirmation,clicked
	confirmation = False
	clicked = False
	MainClass().run()



