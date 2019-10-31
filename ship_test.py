import pygame

class Ship():
	""" корабль """
	def __init__(self, ai_settings, screen):
		self.screen = screen
		self.image = pygame.image.load('images\ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False
		self.ai_settings = ai_settings
		self.center = float(self.rect.centerx)
		self.bottom = float(self.rect.bottom)
		 
	def update(self):
		if self.moving_right == True:
			self.center += self.ai_settings.speed_factor
			if self.center >= self.ai_settings.screen_width - 10:
				self.moving_right = False
		if self.moving_left == True:
			self.center -= self.ai_settings.speed_factor
			if self.center <= 10:
				self.moving_left = False
		self.rect.centerx = self.center
		if self.moving_up:
			self.bottom -= self.ai_settings.speed_factor
			if self.bottom <= 100:
				self.moving_up = False
		if self.moving_down:
			self.bottom += self.ai_settings.speed_factor
			if self.bottom >= 600:
				self.moving_down = False		
		self.rect.bottom = self.bottom
		
	def center_ship(self):
		self.center = self.screen_rect.centerx
		self.bottom = self.screen_rect.bottom
			
	def blitme(self):
		""" рисует корабль """
		self.screen.blit(self.image, self.rect)
