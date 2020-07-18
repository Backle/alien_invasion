class GameStats:
	"""Track Statistics for Alien Invasion"""
	def __init__(self, ai_game):
		"""Initialize Statistics"""
		self.settings = ai_game.settings
		self.reset_stats()

		#start alien invasion in an inactive state
		self.game_active = False

	def reset_stats(self):
		"""" Initializes statistics that can change during the game"""
		self.ships_left = self.settings.ship_limit




