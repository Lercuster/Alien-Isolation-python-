import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	""" корабль """
	def __init__(self, ai_settings, screen):
		super(Alien, self).__init__()
		self.screen = screen
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		self.x = float(self.rect.x)	
		self.speed  = ai_settings.alien_speed
		self.ai_settings = ai_settings
		self.HP = 1
		
	def check_edge(self):
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
			
	def change_color(self):
		self.HP = 0
	
	def update(self):
		self.x += (self.speed * self.ai_settings.fleet_direction)
		self.rect.x = self.x
		
	def blitme(self):
		""" рисует пришельца """
		self.screen.blit(self.image, self.rect)

class AlienRed(Sprite):
	""" корабль """
	def __init__(self, ai_settings, screen):
		super(AlienRed, self).__init__()
		self.screen = screen
		self.image = pygame.image.load('images/alien_red.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		self.x = float(self.rect.x)	
		self.speed  = ai_settings.alien_speed
		self.ai_settings = ai_settings
		self.HP = 2
		
	def check_edge(self):
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
			
	def change_color(self):
		self.image = pygame.image.load('images/alien.bmp')
		self.HP -= 1
		
	def update(self):
		self.x += (self.speed * self.ai_settings.fleet_direction)
		self.rect.x = self.x
		
	def blitme(self):
		""" рисует пришельца """
		self.screen.blit(self.image, self.rect)

class Boss(Sprite):
	""" корабль """
	def __init__(self, ai_settings, screen):
		super(Boss, self).__init__()
		self.screen = screen
		self.image = pygame.image.load('images/boss31.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		self.rect.x = self.rect.width
		self.rect.y = 20
		self.x = float(self.rect.x)	
		self.speed  = ai_settings.alien_speed
		self.ai_settings = ai_settings
		self.HP = 10
		
	def check_edge(self):
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
		
	def update(self):
		self.x += (self.speed * self.ai_settings.fleet_direction)
		self.rect.x = self.x
		
	def change_color(self, t):
		if t == 0:
			self.image = pygame.image.load('images/boss31.bmp')
		elif t == 1:
			self.image = pygame.image.load('images/boss3_2.bmp')
			
		
	def blitme(self):
		""" рисует пришельца """
		self.screen.blit(self.image, self.rect)
