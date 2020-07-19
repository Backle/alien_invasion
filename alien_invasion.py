import sys
from time import sleep
import pygame

from random import randint
from settings import Settings
from ship import Ship
from bullet import Bullet
from bun import Bun
from star import Star
from game_stats import GameStats
from button import Button


class AlienInvasion:
	"""Overall class to manage game assets and behavior."""
	def __init__(self):
		"""Initialize the game, and create game resources."""
		pygame.init()
		self.settings = Settings()
		self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		#create and instance to store game stats
		self.stats = GameStats(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.buns = pygame.sprite.Group()
		self.stars = pygame.sprite.Group()

		self._create_batch()
		self._create_star_sky()

		#make the the Play button
		self.play_button = Button(self, "Play")

		# get the screen dimensions to be used to place buttons
		self.screen_rect = self.screen.get_rect()

		#make the easy button
		self.easy_button = Button(self, "Easy")
		self.easy_button.button_color = (255, 0, 0) #blue
		self.easy_button.rect.centerx = (self.screen_rect.centerx - self.easy_button.width - 50)


		#make the normal button
		self.normal_button = Button(self, "Normal")
		self.normal_button.button_color = (0, 255, 0)  #green
		self.normal_button.rect.center = self.screen_rect.center


		#make the hard button
		self.hard_button = Button(self, "Hard")
		self.hard_button.button_color = (255, 0, 0)  #red
		self.hard_button.rect.centerx = (self.screen_rect.centerx + self.hard_button.width + 50)

		
	def run_game(self):
		"""Start the main loop for the game."""
		while True:
			# Watch for keyboard and mouse events.
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_buns()

			self._update_screen()
		
	def _check_events(self):
		# respond to keyboard and mouse events.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)

			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_keydown_events(self, event):
		"""Respond to keypresses. """
		if event.key == pygame.K_RIGHT:
			# Move the ship to the right.
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			# Move the ship to the left.
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			#Press q to quit
			sys.exit()	
		elif event.key == pygame.K_SPACE:
			#fire bullets on spacebar
			self._fire_bullet()
		elif event.key == pygame.K_p:
			#Press p to start
			if not self.stats.game_active:
				self._start_game()

	def _check_keyup_events(self,event):
		""" respond to key releases."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _start_game(self):
		#Make game active and reset the game stats
			self.stats.reset_stats()
			self.stats.game_active = True

			#get rid of any remaining any buns and bullets
			self.buns.empty()
			self.bullets.empty()

			#create a new batch and center the ship
			self._create_batch()
			self.ship.center_ship()

			# Hide the mouse cursor.
			pygame.mouse.set_visible(False)

	def _check_play_button(self, mouse_pos):
		""" Start a new game when the player clicks Play."""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			#reset the game settings
			self.settings.initialize_dynamic_settings()
			self._start_game()
	
	def _fire_bullet(self):
		""" Create a new bullet and add it to the bullets group"""
		if len(self.bullets)< self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		""" updated bullet position and gets rid of old bullets"""
		#update bullet positons.
		self.bullets.update()
		# get rid of bullets that have dissapeared
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_bun_collision()

	def _check_bullet_bun_collision(self):
		""" Respond to bullet bun collions"""
		collisions = pygame.sprite.groupcollide(self.bullets, self.buns, True, True)
		# Check for any bullets that have hit buns.
        # If so, get rid of the bullet and the bun.
		if not self.buns:
			# Destroy existing bullets and create new fleet.
			self.bullets.empty()
			self._create_batch()
			self.settings.increase_speed()

	def _ship_hit(self):
		"""Respond to the ship being hit by a bun"""

		if self.stats.ships_left > 0:

			#Decrement ships left
			self.stats.ships_left -=1

			#get rid of any remaining buns and bullets
			self.buns.empty()
			self.bullets.empty()

			#create a new batch and center the ship
			self._create_batch()
			self.ship.center_ship()

			#Pause
			sleep(1.5)

		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _create_batch(self):
		""" Create a batch of buns"""
		#Make a bun and find the number of buns in a row
		#spacing between each bun is equal to one bun width
		bun = Bun(self)
		bun_width, bun_height = bun.rect.size
		available_space_x = self.settings.screen_width - (2 * bun_width)
		number_buns_x = available_space_x // (2 * bun_width)

		#determine the number of rows of buns that fit onto the screen.
		ship_height = self.ship.rect.height
		available_space_y =(self.settings.screen_height - (3 * bun_height) - ship_height)
		number_rows = available_space_y // (2 * bun_height)

		# Create the full batch of buns.
		for row_number in range (number_rows):
			for bun_number in range (number_buns_x):
				self._create_bun(bun_number, row_number)

	def _create_bun(self, bun_number, row_number):
			#Create a bun and place it in the row
			bun = Bun(self)
			bun_width, bun_height = bun.rect.size
			bun.x = bun_width + 2 * bun_width * bun_number
			bun.rect.x = bun.x
			bun.rect.y = bun.rect.height + 2 * bun.rect.height * row_number
			self.buns.add(bun)

	def _update_buns(self):
		""" Check is the batch is at an edge, then update the position of all the buns in the batch"""
		self._check_batch_edges()
		self.buns.update()

		# Look for bun / ship collisions
		if pygame.sprite.spritecollideany(self.ship,self.buns):
			self._ship_hit()

		#look for buns hitting the bottom of the screen
		self._check_buns_bottom()

	def _check_batch_edges(self):
		"""Respond appropriately if any buns have reached an edge."""
		for bun in self.buns.sprites():
			if bun.check_edges():
				self._change_batch_direction()
				break

	def _check_buns_bottom(self):
		"""check if any buns have reached the bottom of the screen."""
		screen_rect = self.screen.get_rect()
		for bun in self.buns.sprites():
			if bun.rect.bottom >= screen_rect.bottom:
				#treat this the same as if the ship got hit
				self._ship_hit()
				break

	def _change_batch_direction(self):
		""" Drop the entire batch and change the batch direction. """
		for bun in self.buns.sprites():
			bun.rect.y += self.settings.batch_drop_speed
		self.settings.batch_direction *= -1

	def _create_star_sky(self):
		""" Create a sky full of stars"""
		#Make a star and find the number of stars in a row
		#spacing between each star is equal to one star width
		star = Star(self)
		star_width, star_height = star.rect.size
		available_space_x = self.settings.screen_width
		number_stars_x = available_space_x // star_width // 2

		#determine the number of rows of stars that fit onto the screen.
		available_space_y = self.settings.screen_height
		number_rows = available_space_y // star_height

		# Create the full batch of stars.
		for row_number in range (number_rows):
			random_stars_x = randint (2,14)
			for star_number in range(random_stars_x):
				self._create_star(star_number, row_number)

	def _create_star(self, star_number, row_number):
			#Create a star and place it in the row
			star = Star(self)
			star_width, star_height = star.rect.size
			random_x = randint(0, self.settings.screen_width)
			random_y = randint(0, self.settings.screen_height)
			star.rect.x = random_x
			star.rect.y = random_y
			self.stars.add(star)

	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen."""
		self.screen.fill(self.settings.bg_color)
		self.stars.draw(self.screen)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.buns.draw(self.screen)

		#Draw the play button if the game is inactive.
		if not self.stats.game_active:
				self.play_button.draw_button()
				self.easy_button.draw_button()
		
		pygame.display.flip()

if __name__ == '__main__':
	# Make a game instance, and run the game.
	ai = AlienInvasion()
	ai.run_game()
