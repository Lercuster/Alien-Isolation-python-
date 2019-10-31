import sys
import pygame
from bullet_test import Bullet, BossBullet
from alien_test import Alien, AlienRed, Boss
from time import sleep
from random import choice

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	if event.key == pygame.K_LEFT:
		ship.moving_left = True
	if event.key == pygame.K_UP:
		ship.moving_up = True
	if event.key == pygame.K_DOWN:
		ship.moving_down = True
	if event.key == pygame.K_SPACE:
		if len(bullets) <= ai_settings.bullets_allowed:
			new_bullet = Bullet(ai_settings, screen, ship)
			bullets.add(new_bullet)
	elif event.key == pygame.K_q:
			sys.exit()
	
def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	if event.key == pygame.K_LEFT:
		ship.moving_left = False
	if event.key == pygame.K_UP:
		ship.moving_up = False
	if event.key == pygame.K_DOWN:
		ship.moving_down = False

def check_events(ai_settings, screen, ship, aliens, bullets, stats, play_button, bosses):
	""" обработка нажатий клавиш и мыши """
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)	
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(stats, screen, play_button, mouse_x, mouse_y,
				aliens, bullets, ai_settings, ship, bosses)

def check_play_button(stats, screen, play_button, mouse_x, mouse_y,
	aliens, bullets, ai_settings, ship, bosses):
	butt_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if butt_clicked and not stats.game_active:
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)
		stats.reset_stats()
		stats.game_active = True
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings, screen, aliens, stats, bosses)
		ship.center_ship()
			
def get_alien_number(ai_settings, alien_width):
	available_space = ai_settings.screen_width - 1.7 * alien_width
	alien_numbers = int(available_space / (1.3 * alien_width))
	return alien_numbers
	
def get_row_number(ai_settings, alien_height):
	available_rows = ai_settings.screen_height - 3 * alien_height
	row_numbers = int(available_rows / (2 * alien_height))
	return row_numbers

def create_alien(ai_settings, screen, aliens, typee, alien_number, row_number):
	if typee == 1:
		alien = Alien(ai_settings, screen)
	elif typee == 2:
		alien = AlienRed(ai_settings, screen)
	alien_width = alien.rect.width
	alien_height = alien.rect.height
	alien.x = 50 + 1.3 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.y = 0 + 1.5*alien_height * row_number
	alien.rect.y = alien.y
	aliens.add(alien)

def create_fleet(ai_settings, screen, aliens, stats, bosses):
	if stats.boss_fight == True:
		boss = Boss(ai_settings, screen)
		bosses.add(boss)
	else:
		alien = Alien(ai_settings, screen)
		alien_numbers = get_alien_number(ai_settings, alien.rect.width)
		row_numbers = get_row_number(ai_settings, alien.rect.height)
		for row_num in range(row_numbers):
			for alien_num in range(0, alien_numbers):
				typee = choice([1, 1, 1, 2])
				create_alien(ai_settings, screen, aliens, typee, alien_num, row_num)

def update_screen(ai_settings, screen, ship, alien, bullets, stats, 
	play_button, boss, bossbullets):
	""" обновляет изображение на жкране и отображает его """
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	for bullet in bossbullets.sprites():
		bullet.draw_bullet()
	if stats.boss_fight:
		boss.draw(screen)
	else:
		alien.draw(screen)
	if not stats.game_active:
		play_button.draw_button()
	pygame.display.flip()

def update_aliens(ai_settings, screen, aliens, bullets, ship, stats, bosses):
	check_fleet_direction(ai_settings, aliens)
	aliens.update()
	check_aliens_bottom(ai_settings, screen, aliens, bullets, ship, stats, bosses)
	if pygame.sprite.spritecollideany(ship, aliens):
		#print('JI O X ')
		ship_hit(ai_settings, screen, aliens, bullets, ship, stats, bosses)
			

def ship_hit(ai_settings, screen, aliens, bullets, ship, stats, bosses):
	if stats.ships_left > 0:
		stats.ships_left -= 1
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings, screen, aliens, stats, bosses)
		ship.center_ship()
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		
def check_fleet_direction(ai_settings, aliens):
	for alien in aliens.sprites():
		if alien.check_edge():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.alien_drop
	ai_settings.fleet_direction = ai_settings.fleet_direction * (-1)

def check_b_a_collisions(ai_settings, screen, aliens, bullets, stats, bosses):
	if stats.boss_fight:
		fleet = bosses.copy()
		collisions = pygame.sprite.groupcollide(fleet, bullets, False, True)
		if collisions:
			for boss in collisions.keys():
				boss.HP -= 1
				if boss.HP == 0:
					boss.kill()		
	else:
		fleet = aliens.copy()
		collisions = pygame.sprite.groupcollide(fleet, bullets, False, True)
		if collisions:
			for alien in collisions.keys():
				alien.change_color()
				if alien.HP == 0:
					alien.kill()
	if (len(aliens) + len(bosses)) == 0:
		print(len(bosses))
		bullets.empty()
		ai_settings.increase_speed()
		stats.level += 1
		print(stats.level)
		if stats.level % 2 == 0:
			stats.boss_fight = True
			create_fleet(ai_settings, screen, aliens, stats, bosses)
		else:
			stats.boss_fight = False
			create_fleet(ai_settings, screen, aliens, stats, bosses)

def check_aliens_bottom(ai_settings, screen, aliens, bullets, ship, stats, bosses):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom - 20:
			ship_hit(ai_settings, screen, aliens, bullets, ship, stats, bosses)
			break

def update_bullets(ai_settings, screen, aliens, bullets):
	bullets.update()
	#print(len(bullets))
	
def change_boss_direction(ai_settings, bosses):
	ai_settings.fleet_direction = ai_settings.fleet_direction * (-1)
	
def check_boss_direction(ai_settings, aliens):
	for alien in aliens.sprites():
		if alien.check_edge():
			change_boss_direction(ai_settings, aliens)
			break

def update_boss(ai_settings, screen, bullets, bosses):
	check_boss_direction(ai_settings, bosses)
	bosses.update()
	
def boss_shot(ai_settings, ship, screen, bossbullets, boss):
	bossbullet = BossBullet(ai_settings, screen, boss)
	bossbullets.add(bossbullet)
	
def update_bossbullets(ai_settings, screen, bossbullets, bosses):
	bossbullets.update()
	
