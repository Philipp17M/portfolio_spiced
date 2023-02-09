#!/usr/bin/env python
# coding: utf-8

#################################################################################################################
### Code for Snake-Game here taken from: https://www.geeksforgeeks.org/snake-game-in-python-using-pygame-module/
#################################################################################################################

# importing libraries
import pygame
import time
import random
import math
import numpy as np

class Snake_game():

	# window size
	window_x = 300
	window_y = 300
	# defining colors
	black = pygame.Color(0, 0, 0)
	white = pygame.Color(255, 255, 255)
	red = pygame.Color(255, 0, 0)
	green = pygame.Color(0, 255, 0)
	blue = pygame.Color(0, 0, 255)
	yellow = pygame.Color(255, 255, 0)
	# game over penalties
	penalty_body = -10
	penalty_wall = -10
	# distance rewards
	reward_closer = 1
	reward_further = -1
	# apple reward
	reward_apple = 10

	def __init__(self, architecture = 'simple'):
		
		self.action_space = 4
		self.state_space = 16
		self.architecture = architecture
		if self.architecture == 'complex':
			self.state_space = ((self.window_x//10+2) * (self.window_y//10+2))
		elif self.architecture == 'complex_cnn':
			self.state_space = ((self.window_x//5), (self.window_y//5), 3)
		self.snake_speed = 15
		self.steps_total = 1
		self.reward = 0
		# init pygame
		pygame.init()
		pygame.font.init()
		# Initialise game window
		pygame.display.set_caption('AI reinforced Snakes')
		self.game_window = pygame.display.set_mode((self.window_x, self.window_y))
		self.rgb_array = pygame.surfarray.array3d(self.game_window)
		self.rgb_array = self.rgb_array[::5,::5,:]
		# FPS (frames per second) controller
		self.fps = pygame.time.Clock()
		# defining snake default position
		self.snake_position = [100, 50]

		# defining first 4 blocks of snake body
		self.snake_body = [[100, 50],
			[90, 50],
			[80, 50],
			[70, 50]
			]
		# fruit position
		self.fruit_position = [random.randrange(1, (self.window_x//10)) * 10,
				random.randrange(1, (self.window_y//10)) * 10]
		self.fruit_spawn = True
		# calc distance btw fruit and head
		self.dist = math.sqrt((self.snake_position[0]-self.fruit_position[0])**2 + (self.snake_position[1]-self.fruit_position[1])**2)
		# setting default snake direction towards
		# right
		self.direction = 'RIGHT'
		self.change_to = self.direction

		# initial score
		self.score = 0
		# initialize highscore
		self.highscore = 0
		# reset game-over flag
		self.done = False

	# function defs

	def reset(self):
		# reset game over flag
		self.done = False
		# defining snake default position
		self.snake_position = [100, 50]
		# defining first 4 blocks of snake body
		self.snake_body = [[100, 50],
			[90, 50],
			[80, 50],
			[70, 50]
			]
		# fruit position
		self.fruit_position = [random.randrange(1, (self.window_x//10)) * 10,
				random.randrange(1, (self.window_y//10)) * 10]
		self.fruit_spawn = True
		# setting default snake direction towards
		# right
		self.direction = 'RIGHT'
		self.change_to = self.direction
		self.score = 0
		self.reward = 0
		self.done = False
		# reset screen
		self.game_window.fill(self.black)
		# draw screen
	#	i = 0
		#for pos in self.snake_body:
	#		if i == 0:
	#			pygame.draw.rect(self.game_window, self.yellow,
	#						pygame.Rect(pos[0], pos[1], 10, 10))
	#		else:
	#			pygame.draw.rect(self.game_window, self.green,
	#						pygame.Rect(pos[0], pos[1], 10, 10))
	#	pygame.draw.rect(self.game_window,self.white, pygame.Rect(
	#		self.fruit_position[0], self.fruit_position[1], 10, 10))
	#	pygame.draw.lines(self.game_window, self.red, closed=True, points=[(0,0),(0,self.window_y),(self.window_x, self.window_y),(self.window_x,0)])
		return self.get_state()

	# displaying Score function
	def show_score(self, choice, color, font, size):
		# creating font object score_font
		score_font = pygame.font.SysFont(font, size)
		# create the display surface object
		# score_surface
		score_surface = score_font.render('Score : ' + str(self.score) + '  Highscore : ' + str(self.highscore), True, color)
		# create a rectangular object for the text
		# surface object
		score_rect = score_surface.get_rect()
		# displaying text
		self.game_window.blit(score_surface, score_rect)

	# game over function
	def game_over(self, reason):
		# setting flag
		self.done = True
		# set highscore
		if self.score > self.highscore:
			self.highscore = self.score
		# setting game over penalty
		if reason == 'body':
			self.reward = self.penalty_body
		else:
			self.reward = self.penalty_wall
		# creating font object my_font
		my_font = pygame.font.SysFont('timesnewroman', 20)
		# creating a text surface on which text
		# will be drawn
		game_over_surface = my_font.render(
			'Your Score is : ' + str(self.score), True, self.red)
		# create a rectangular object for the text
		# surface object
		game_over_rect = game_over_surface.get_rect()
		# setting position of the text
		game_over_rect.midtop = (self.window_x/2, self.window_y/4)
		# blit will draw the text on screen
		self.game_window.blit(game_over_surface, game_over_rect)
		pygame.display.flip()
		# after 2 seconds we will quit the program
		time.sleep(0.5)
		# deactivating pygame library
		#pygame.quit()
		# quit the program
		#quit()

	def measure_distance(self):
		self.prev_dist = self.dist
		# self.snake_position[0] = [100, 50]
		self.dist = math.sqrt((self.snake_position[0]-self.fruit_position[0])**2 + (self.snake_position[1]-self.fruit_position[1])**2)


	def get_state(self):
		
		if self.architecture == 'simple':
			# wall checks
			if self.snake_position[1] >= self.window_y-10:
				wall_up, wall_down = 1, 0
			elif self.snake_position[1] <= 0:
				wall_up, wall_down = 0, 1
			else:
				wall_up, wall_down = 0, 0
			
			if self.snake_position[0] >= self.window_x-10:
				wall_right, wall_left = 1, 0
			elif self.snake_position[0] <= 0:
				wall_right, wall_left = 0, 1
			else:
				wall_right, wall_left = 0, 0
				
			# body close and loop detection:
			body_up = 0
			body_right = 0
			body_down = 0
			body_left = 0

			loop_up = 0
			loop_right = 0
			loop_down = 0
			loop_left = 0

			old_piece = self.snake_body[2]
			for piece in self.snake_body[3:]:
				delta_x = piece[0] - old_piece[0]
				delta_y = piece[1] - old_piece[1]
				old_piece = piece
				if piece[0] == self.snake_position[0] + 10 and piece[1] == self.snake_position[1]:
					body_right = 1
					if delta_y > 0:
						loop_up = 1
					else:
						loop_down = 1
				if piece[0] == self.snake_position[0] - 10 and piece[1] == self.snake_position[1]:
					body_left = 1
					if delta_y > 0:
						loop_up = 1
					else:
						loop_down = 1
				if piece[1] == self.snake_position[1] + 10 and piece[0] == self.snake_position[0]:
					body_down = 1
					if delta_x < 0:
						loop_right = 1
					else:
						loop_left = 1
				if piece[1] == self.snake_position[1] - 10 and piece[0] == self.snake_position[0]:
					body_up = 1
					if delta_x < 0:
						loop_right = 1
					else:
						loop_left = 1

			# construct state
			state = [int(self.snake_position[1] < self.fruit_position[1]), int(self.snake_position[0] < self.fruit_position[0]), int(self.snake_position[1] > self.fruit_position[1]), int(self.snake_position[0] > self.fruit_position[0]), \
						int(wall_up or body_up), int(wall_right or body_right), int(wall_down or body_down), int(wall_left or body_left), \
						loop_up, loop_right, loop_down, loop_left, \
						int(self.direction == 'UP'), int(self.direction == 'RIGHT'), int(self.direction == 'DOWN'), int(self.direction == 'LEFT')]
		
		elif self.architecture == 'complex':
			state = np.zeros((self.window_x//10+2, self.window_y//10+2))
			for pos in self.snake_body:
				state[pos[0]//10+1, pos[1]//10+1] = 1
			state[self.snake_position[0]//10+1, self.snake_position[1]//10+1] = 2
			state[self.fruit_position[0]//10+1, self.fruit_position[1]//10+1] = 3

		elif self.architecture == 'complex_cnn':
			self.rgb_array = pygame.surfarray.array3d(self.game_window)
			state = self.rgb_array[::5,::5,:]
			

		return state
		#pass



## ADD: function that returns state

## EDIT: act() should return the reward of the action


	# Main Function

	def step(self, action):

		self.steps_total += 1
		# handling key events
		if action == 0:
			self.change_to = 'UP'
		elif action == 1:
			self.change_to = 'RIGHT'
		elif action == 2:
			self.change_to = 'DOWN'
		elif action == 3:
			self.change_to = 'LEFT'

		# If two keys pressed simultaneously
		# we don't want snake to move into two
		# directions simultaneously
		if self.change_to == 'UP' and self.direction != 'DOWN':
			self.direction = 'UP'
		if self.change_to == 'DOWN' and self.direction != 'UP':
			self.direction = 'DOWN'
		if self.change_to == 'LEFT' and self.direction != 'RIGHT':
			self.direction = 'LEFT'
		if self.change_to == 'RIGHT' and self.direction != 'LEFT':
			self.direction = 'RIGHT'

		# Moving the snake
		if self.direction == 'UP':
			self.snake_position[1] -= 10
		if self.direction == 'DOWN':
			self.snake_position[1] += 10
		if self.direction == 'LEFT':
			self.snake_position[0] -= 10
		if self.direction == 'RIGHT':
			self.snake_position[0] += 10

		# Snake body growing mechanism
		# if fruits and snakes collide then scores
		# will be incremented by 10
		self.snake_body.insert(0, list(self.snake_position))
		if self.snake_position[0] == self.fruit_position[0] and self.snake_position[1] == self.fruit_position[1]:
			self.score += 10
			self.reward = self.reward_apple
			self.fruit_spawn = False
		else:
			self.snake_body.pop()
			self.measure_distance()
			if self.dist < self.prev_dist:
				self.reward = self.reward_closer
			else:
				self.reward = self.reward_further
			self.reward *= (1 if 800/self.steps_total > 1 else np.max((800/self.steps_total, 0.1)))
		# spawn fruit or not, if yes give apple reward if no give reward based on distance
		if not self.fruit_spawn:
			self.fruit_position = [random.randrange(1, (self.window_x//10)) * 10,
							random.randrange(1, (self.window_y//10)) * 10]
			
		self.fruit_spawn = True
		self.game_window.fill(self.black)
		i = 0
		for pos in self.snake_body:
			if i == 0:
				pygame.draw.rect(self.game_window, self.yellow,
							pygame.Rect(pos[0], pos[1], 10, 10))
			else:
				pygame.draw.rect(self.game_window, self.green,
							pygame.Rect(pos[0], pos[1], 10, 10))
			i += 1
		pygame.draw.rect(self.game_window,self.white, pygame.Rect(
			self.fruit_position[0], self.fruit_position[1], 10, 10))
		pygame.draw.lines(self.game_window, self.red, closed=True, points=[(0,0),(0,self.window_y),(self.window_x, self.window_y),(self.window_x,0)], width=5)
		self.rgb_array = pygame.surfarray.array3d(self.game_window)
		# Game Over conditions
		if self.snake_position[0] < 0 or self.snake_position[0] > self.window_x-10:
			self.game_over('wall')
		if self.snake_position[1] < 0 or self.snake_position[1] > self.window_y-10:
			self.game_over('wall')

		# Touching the snake body
		for block in self.snake_body[1:]:
			if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
				self.game_over('body')

		# displaying score countinuously
		self.show_score(1, self.white, 'timesnewroman', 20)

		# Refresh game screen
		pygame.display.update()
		#This will pump the event queue and close the window and program
		#if the user clicks the close button of the window
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				raise SystemExit

		state = self.get_state()

		return state, self.reward, self.done, {}

		# Frame Per Second /Refresh Rate
		#self.fps.tick(self.snake_speed)
