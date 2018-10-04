import kivy

from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.config import Config

import numpy as np

def fill_place(main_grid,smll_grid,row_col):
	global grid_solved
	if(row_col == 81):
		global solved_grid
		solved_grid = main_grid.copy()
		grid_solved = True
		return
	else:
		row = int(row_col/9)
		col = int(row_col%9)
		if(main_grid[row][col]==0 and not(grid_solved)):
			for i in range(1,10):
				if not grid_solved:
					if not (i in main_grid[row,:]):
						if not (i in main_grid[:,col]):
							if not (i in smll_grid[(3)*(row//(3))+(col//3),:]):
								main_grid_copy = main_grid.copy()
								smll_grid_copy = smll_grid.copy()
								main_grid_copy[row,col] = i
								smll_grid_copy[(3)*(row//(3))+(col//3),(3*(row%3)+(col%3))] = i
								fill_place(main_grid_copy.copy(),smll_grid_copy.copy(),row_col+1)
				else:
					return
		elif grid_solved:
			return
		else:
			fill_place(main_grid.copy(),smll_grid.copy(),row_col+1)

class MainScreen(Screen):
	def __init__(self,**kwargs):
		super(MainScreen,self).__init__(**kwargs)
		self.btn_sep = 0.004
		self.sqr_sep = 0.006
		self.end_sep = 0.01
		self.button_size = (1-(2*self.end_sep)-(9*self.btn_sep)-(2*self.sqr_sep))/9
		self.build_grid()
		self.solve_btn = Button(text="SOLVE",font_size=30,size_hint=(0.5,(1.0/6)),pos_hint={"center_x":(0.75), "center_y":(1.0/12)},on_release=(self.goto_solve))
		self.add_widget(self.solve_btn)
		self.clear_btn = Button(text="CLEAR",font_size=30,size_hint=(0.5,(1.0/6)),pos_hint={"center_x":(0.25), "center_y":(1.0/12)},on_release=(self.goto_clear))
		self.add_widget(self.clear_btn)

	def goto_solve(self,_):
		global solved_grid, grid_solved
		all_grid = np.zeros((9,9),dtype=int)
		sqr_grid = np.zeros((9,9),dtype=int)
		solved_grid = np.zeros((9,9),dtype=int)
		for i in range(9):
			for j in range(9):
				x = (self.all_ins[i*9+j].text)
				if (x == ""):
					x=0
				else:
					print(i,j,x)
					try:
						x = int(x)
						print(x)
					except:
						x = 0
					if(not(0<x<10)):
						x=0
					else:
						sqr_grid[(3)*(i//(3))+(j//3),(3*(i%3)+(j%3))] = x
				all_grid[i][j] = x
		print(all_grid)
		grid_solved = False
		fill_place(all_grid,sqr_grid,0)
		print(solved_grid)
		for i in range(9):
			for j in range(9):
				self.all_ins[i*9+j].text = str(solved_grid[i][j])

	def goto_clear(self,_):
		for i in range(9):
			for j in range(9):
				self.all_ins[j*9+i].text = str("")

	def build_grid(self):
		now_input = TextInput(font_size=30,size_hint=(self.button_size,(5.0/6.0)*self.button_size),pos_hint={"center_x":0.5, "center_y":0.5})
		self.all_ins = [now_input for i in range(81)]
		for j in range(9):
			for i in range(9):
				my_id = "val" + str(i*9+j)
				x_cen = self.end_sep + (i//3)*self.sqr_sep + (i+0.5)*(self.button_size+self.btn_sep)
				y_cen = 1 - (5.0/6.0)*(self.end_sep + (j//3)*self.sqr_sep + (j+0.5)*(self.button_size+self.btn_sep))
				self.all_ins[i*9+j] = TextInput(font_size=30,size_hint=(self.button_size,(5.0/6.0)*self.button_size),pos_hint={"center_x":x_cen, "center_y":y_cen})
				self.add_widget(self.all_ins[i*9+j])

class MainClass(App):
	def build(self):
		Config.set('graphics', 'resizable', '0') #0 being off 1 being on as in true/false
		Config.set('graphics', 'width', '500')
		Config.set('graphics', 'height', '600')

		ScreenMan = ScreenManagerbuild()

		ScreenMan.add_widget(MainScreen(name='mainhome_window'))
		
		return ScreenMan

class ScreenManagerbuild(ScreenManager):
	pass

global grid_solved, solved_grid
grid_solved = False
all_grid = np.zeros((9,9),dtype=int)
sqr_grid = np.zeros((9,9),dtype=int)
solved_grid = np.zeros((9,9),dtype=int)

all_grid[0][0]=2
sqr_grid[0][0]=2
fill_place(all_grid,sqr_grid,0)
print(solved_grid)

if __name__ == '__main__':
	MainClass().run()




print(solved_grid)



