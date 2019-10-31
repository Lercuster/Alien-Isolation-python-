import sys
import pygame 
from settings_test import Settings
from ship_test import Ship
import game_functions_test as gf
from pygame.sprite import Group
from alien_test import Alien, AlienRed, Boss
from game_stats_test import GameStats
from button_test import Button

def run_game():
	pygame.init()
	i = 0
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, 
		ai_settings.screen_height))
	pygame.display.set_caption('alien_isolation')
	ship = Ship(ai_settings, screen)
	alien = Alien(ai_settings, screen)
	bullets = Group()
	aliens = Group()
	bosses = Group()
	bossbullets = Group()
	stats = GameStats(ai_settings)
	play_button = Button(ai_settings, screen, 'Play')
	gf.create_fleet(ai_settings, screen, aliens, stats, bosses)
	while True:
		gf.check_events(ai_settings, screen, ship, aliens, bullets, stats, 
			play_button, bosses)
		if stats.game_active:
			ship.update()
			gf.check_b_a_collisions(ai_settings, screen, aliens, bullets, stats, bosses)
			gf.update_bullets(ai_settings, screen, aliens, bullets)
			if stats.boss_fight:
				i += 1
				gf.update_boss(ai_settings, screen, bullets, bosses)
				gf.update_bossbullets(ai_settings, screen, bossbullets, bosses)
				for boss in bosses:
					if i % 500 == 0:
						gf.boss_shot(ai_settings, ship, screen, bossbullets, boss)
						boss.change_color(0)
					elif i % 500 == 250:
						boss.change_color(1)						
			else:
				gf.update_aliens(ai_settings, screen, aliens, bullets, ship, stats, bosses)
			for bullet in bullets.copy():
				if bullet.rect.bottom <= 0:
					bullets.remove(bullet) 
			for bullet in bossbullets.copy():
				if bullet.rect.bottom >= ai_settings.screen_height:
					bossbullets.remove(bullet)
		gf.update_screen(ai_settings, screen, ship, aliens, bullets,
				stats, play_button, bosses, bossbullets)
run_game()
