class GameStats:
	"""Track Statistics for Alien Invasion"""
	def __init__(self, ai_game):
		"""Initialize Statistics"""
		self.settings = ai_game.settings
		self.reset_stats()

		#start alien invasion in an inactive state
		self.game_active = False

		#initalize high score from saved file value
		with open('high_score.txt') as f:
			self.high_score = int(f.read())

	def reset_stats(self):
		"""" Initializes statistics that can change during the game"""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1




