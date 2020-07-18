import pygame
from pygame.sprite import Sprite

class Bun(Sprite):
	""" A class to represent a single bun in the batch"""

	def __init__ (self, ai_game):
		""" Initialize the bun and set its starting position"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		#load the bun and set its rect attribute.
		self.image = pygame.image.load('images/hc_bun.png')
		self.rect = self.image.get_rect()

		#start each new bun near the top left of the screen.
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#store the bun's exact horizontal position.
		self.x = float(self.rect.x)

	def check_edges(self):
		""" Return True if bun is at the edge of the screen"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		if self.rect.left <= 0:
			return True

	def update(self):
		""" Move the bun to the right """
		self.x += (self.settings.bun_speed * self.settings.batch_direction)
		self.rect.x = self.x

