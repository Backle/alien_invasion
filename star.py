import pygame
from pygame.sprite import Sprite

class Star(Sprite):
	""" A class to represent a single star in the batch"""

	def __init__ (self, ai_game):
		""" Initialize the star and set its starting position"""
		super().__init__()
		self.screen = ai_game.screen

		#load the star and set its rect attribute.
		self.image = pygame.image.load('images/star.png')
		self.rect = self.image.get_rect()

		#start each new star near the top left of the screen.
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#store the star exact horizontal position.
		self.x = float(self.rect.x)
