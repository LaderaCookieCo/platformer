#made by tmk2-0
from re import A
import pygame
from random import randint as rand
from pygame.locals import *
from time import sleep as sl
import math as m
vec = pygame.math.Vector2

pygame.init()
FPS = 60
WIDTH = 720
HEIGHT = 480
ACC = 0.5
MAXJ = 3
fric = -0.12
size = (WIDTH, HEIGHT)
displaySurface = pygame.display.set_mode(size, pygame.RESIZABLE)
framePerSec = pygame.time.Clock()
f = pygame.font.SysFont("SourceCodePro-Bold", 24)
f64 = pygame.font.SysFont("SourceCodePro-Bold", 64)
killtimer = 0
killtcap = 120
gamestate = True



def gameover():
	global all_sprites
	for s in all_sprites:
		s.kill()
	global gamestate
	gamestate = False

class Platform(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.surf = pygame.Surface((rand(50, 100), 12))
		self.surf.fill((250, rand(20, 100), 70))
		self.rect = self.surf.get_rect(center = (rand(0, WIDTH), rand(0, (HEIGHT - 200))))
		self.speed = rand(-1, 1)
	
	def move(self):
		self.rect.x += self.speed
		if self.rect.center[0] < (-self.rect.width/2):
			self.rect.x = (WIDTH)
		if self.rect.center[0] > (WIDTH + self.rect.width/2):
			self.rect.x = (-self.rect.width)

	def update(self):
		pass



class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.surf = pygame.Surface((30, 30))
		self.surf.fill((12, 255, 120))
		self.rect = self.surf.get_rect()
		self.pos = vec(40, HEIGHT/1.32)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)
		self.jumpcount = 0
		self.score = 0
		self.plat = None
		
	def move(self):
		self.acc = vec(0, ACC)
		keys_pressed = pygame.key.get_pressed()
		if keys_pressed[K_LEFT] or keys_pressed[K_a]:
			self.acc.x = -ACC
		if keys_pressed[K_RIGHT] or keys_pressed[K_d]:
			self.acc.x = ACC
		self.acc.x += self.vel.x * fric
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc
		if not self.plat:
			if self.pos.x < (-15):
				self.pos.x = (WIDTH + 15)
			if self.pos.x > (WIDTH + 15):
				self.pos.x = (-15)
		self.rect.midbottom = self.pos

	def update(self):
		hits = pygame.sprite.spritecollide(self, platforms, False)
		self.plat = None
		if self.vel.y >0:
			if hits and self.rect.y < hits[0].rect.center[1]:
				self.vel.y = 0
				self.jumpcount = 0
				self.pos.y = hits[0].rect.top + 1
				self.pos.x += hits[0].speed
				self.plat = hits[0]
			

	def jump(self):
		if self.jumpcount < MAXJ:
			self.vel.y -= 15
			self.jumpcount += 1
		
	def cancel_jump(self):
		if self.vel.y < -5:
			self.vel.y = -5

class EvilPlayer (Player):
	def __init__(self):
		super().__init__()
		self.vel = vec(0, 0)
		self.acc = vec(0, ACC)
		self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT/1.32))
		self.surf.fill((255, 255, 0))
		self.speed = 0.3
	def move(self):
		self.acc = vec(0, ACC)
		self.acc.x += self.vel.x * fric
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc
		if not self.plat:
			if self.pos.x < (-15):
				self.pos.x = (WIDTH + 15)
			if self.pos.x > (WIDTH + 15):
				self.pos.x = (-15)
		self.rect.midbottom = self.pos
	def jump(self):
		if self.jumpcount < MAXJ:
			self.vel.y -= 15
			self.jumpcount += 1
	def cancel_jump(self):
		pass

#evil player physics

	def eupdate(self, p1, platforms):
		closestp = self.closestplatform(platforms)
		jumpmovechance = rand(1, 10000)

		if jumpmovechance == 1:
			self.jumpadv(platforms.sprites()[closestp])

	def jumpadv(self, dest):
		jtime = 0.2
		h = dest.rect.y - self.pos.y
		xpos = dest.rect.x - self.pos.x
		yv = m.sqrt(2 * ACC * m.fabs(h))
		xv = xpos/jtime
		self.vel = vec(xv, yv)
		
#platform closeness checker

	def closestplatform(self, platforms):
		min = m.sqrt(pow(platforms.sprites()[0].rect.y - self.pos.y, 2) + pow(platforms.sprites()[0].rect.x - self.pos.x, 2))
		minindex = 0
		for i, platform in enumerate(platforms.sprites()):
			dist = m.sqrt(pow(platform.rect.y - self.pos.y, 2) + pow(platform.rect.x - self.pos.x, 2))
			if dist < min:
				min = dist
				minindex = i
		return minindex

def plat_gen(min = 0, max = -50):
	while len(platforms) < 7:
		width = rand(50,100)
		p = None
		C = True
		i = 0
		while C and i < 50:
			p = Platform()
			x = rand(width//2, WIDTH-width//2)
			y = rand(max, min)
			p.rect.center = (x, y)
			C = check(p, platforms)
			i += 1
		if not i < 50:
			break
		platforms.add(p)
		all_sprites.add(p)

def check(platform, group):
	if pygame.sprite.spritecollideany(platform, group):
		return True
	else:
		for entity in group:
			if entity == platform:
				continue
			difUp = abs(platform.rect.top - entity.rect.bottom)
			difDown = abs(platform.rect.top - entity.rect.bottom)
			if difUp < 50 and difDown < 50:
				return True
		return False

pt1 = None
p1 = None
platforms = None
all_sprites = None

def startnew():
	global pt1
	global p1
	global platforms
	global all_sprites
	global gamestate
	global killtimer
	global ep
	ep = EvilPlayer()
	pt1 = Platform()
	pt1.surf = pygame.Surface(((WIDTH + 100), 200))
	pt1.surf.fill((27, 200, 4))
	pt1.speed = 0
	pt1.rect = pt1.surf.get_rect(topleft = (0, int(HEIGHT)/1.32))
	platforms = pygame.sprite.Group()

	all_sprites = pygame.sprite.Group()

	plat_gen(HEIGHT, 0)

	platforms.add(pt1)
	all_sprites.add(pt1)
	all_sprites.add(ep)

	p1 = Player()
	all_sprites.add(p1)

	gamestate = True
	killtimer = 0

startnew()

while True:
	for event in pygame.event.get():
		if event.type == pygame.VIDEORESIZE:
			WIDTH, HEIGHT = event.w, event.h
			old_surface_saved = displaySurface
			displaySurface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
			pt1.surf = pygame.Surface((WIDTH, 300))
			pt1.surf.fill((27, 200, 4))
			pt1.rect.width = WIDTH
			pt1.rect.midbottom = ((WIDTH/2), HEIGHT)
		if event.type == QUIT:
			pygame.quit()
		if event.type == KEYDOWN and gamestate:
			if event.key == K_UP or event.key == K_w or event.key == K_SPACE:
				p1.jump()
		if event.type == KEYUP and gamestate:
			if event.key == K_UP or event.key == K_w or event.key == K_UP or event.key == K_SPACE:
				p1.cancel_jump()		

	if gamestate:
		displaySurface.fill((0, 0, 0))
		plat_gen()
		for sprite in all_sprites:
			displaySurface.blit(sprite.surf, sprite.rect)
			sprite.move()
			sprite.update()
		ep.eupdate(p1, platforms)
		scoresurf = f.render(str(p1.score//10), True, (255, 255, 255))
		displaySurface.blit(scoresurf,(WIDTH/30, 20))
		if p1.rect.top <= HEIGHT/3:
			p1.pos.y += abs(p1.vel.y)
			p1.score += 1
			for plat in platforms:
				plat.rect.y += abs(p1.vel.y)
				if plat.rect.top >= HEIGHT:
					plat.kill()
		if p1.rect.top > HEIGHT:
			gameover()
	else:
		killtimer += 1
		if killtimer >= killtcap:
			done = False
			scend = f64.render(str((p1.score//10)), True, (255, 255, 255))
			pressakey = f64.render(str("Press any Key to Continue"), True, (255, 255, 255))
			while not done:
				displaySurface.fill((0, 0, 0))
				displaySurface.blit(scend, (WIDTH/2 - scend.get_width()/2, HEIGHT/2 - scend.get_height()/2))
				displaySurface.blit(pressakey, (WIDTH/2 - pressakey.get_width()/2, HEIGHT/3))
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == QUIT:
						pygame.quit()
					if event.type == KEYDOWN:
						done = True
						startnew()
		elif killtimer % 12 == 0 and killtimer < 120:
			displaySurface.fill((0, 0, (displaySurface.get_at((0, 0))[2] + 127) % 255))
	pygame.display.update()
	framePerSec.tick(FPS)