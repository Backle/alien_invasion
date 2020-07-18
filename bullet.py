import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
	""" A class to manage bullets fired from the ship"""
	def __init__(self, ai_game):
		"""create a bullet object at the ship's current position"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color

		# create a bullet at rect (0,0) and then set the correct position
		self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
		baguette_aduster = int(ai_game.ship.rect.x) + 56
		self.rect.midtop = (baguette_aduster,ai_game.ship.rect.y)

		#store the bullet's position as a decimal value
		self.y = float(self.rect.y)

	def update(self):
		"""Move the bullet up the screen"""
		#update the decimal position of the bullet.
		self.y -=self.settings.bullet_speed
		#update the rect positon.
		self.rect.y = self.y

	def draw_bullet(self):
		"""Draw the bullet to the screen."""
		pygame.draw.rect(self.screen, self.color, self.rect)