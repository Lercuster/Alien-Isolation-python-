class Settings():
	""" класс настроек игры"""
	def __init__(self):
		""" инициализируем настройки игры """
		self.screen_width = 1300
		self.screen_height = 600
		self.bg_color = (255, 255, 255)
		self.bullet_color = (60, 60, 60)
		self.bullet_width = 6
		self.bullet_height = 6
		self.bossbullet_width = 15
		self.bossbullet_height = 10
		self.bullets_allowed = 2
		self.alien_drop = 15
		self.ship_limit = 3
		self.speed_scale = 1.1
		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		self.speed_factor = 0.7
		self.bullet_speed = 1
		self.alien_speed = 0.4
		self.fleet_direction = 1
		
	def increase_speed(self):
		self.alien_speed *= self.speed_scale 
		
