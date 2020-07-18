class Settings:
	"""A class to store all settings for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's static settings."""
		# Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (3, 41, 120)

		#Ship Settings
		self.ship_limit = 3

		# Bullet settings
		self.bullet_width = 5
		self.bullet_height = 15
		self.bullet_color = (191, 122, 70)
		self.bullets_allowed = 3

		# Bun settings
		self.bun_speed = 1.0
		self.batch_drop_speed = 10

		#Batch direction of 1 represents right; -1 represents left.
		self.batch_direction = 1

		# How quickly the game speeds up
		self.speedup_scale = 1.25

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize settings that can change througout the game"""
		self.ship_speed = 5
		self.bullet_speed = 5
		self.bun_speed = 3

		# batch_direction of 1 represents rigth; -1 represents left
		self.batch_direction = 1

	def increase_speed(self):
		"""Increase speed settings"""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.bun_speed *= self.speedup_scale

