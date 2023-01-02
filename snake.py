import pygame, sys, random
from pygame import gfxdraw
from pygame.math import Vector2

GREEN = (173,204,96)
DARK_GREEN = (43,51,24)

pygame.init()
title_font = pygame.font.Font(None, 50)
score_font = pygame.font.Font(None, 30)

cell_size = 28
cell_number = 20
OFFSET = 50

class FOOD:
	def __init__(self):
		self.pos = self.generate_random_pos()

	def draw(self):
		food_rect = pygame.Rect(OFFSET + self.pos.x * cell_size, OFFSET + self.pos.y * cell_size, cell_size, cell_size)
		screen.blit(food, food_rect)

	def recreate(self, snake_body):
		self.pos = self.generate_random_pos()
		while self.pos in snake_body:
			self.pos = self.generate_random_pos()

	def generate_random_pos(self):
		x = random.randint(0,cell_number-1)
		y = random.randint(0,cell_number-1)
		pos = Vector2(x, y)
		return pos

class SNAKE:
	def __init__(self):
		self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
		self.direction = Vector2(1,0)
		self.add_segment = False

	def draw(self):
		for segment in self.body:
			pygame.draw.rect(screen, DARK_GREEN, (OFFSET + segment.x*cell_size, OFFSET + segment.y*cell_size,cell_size, cell_size), 0 , 7)

	def update(self):
		if self.add_segment:
			self.body.insert(0, self.body[0] + self.direction)
			self.add_segment = False
		else:
			self.body = self.body[:-1]
			self.body.insert(0, self.body[0] + self.direction)

	def reset(self):
		self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
		self.direction = Vector2(1, 0)

class GAME:
	def __init__(self):
		self.snake = SNAKE()
		self.food = FOOD()
		self.state = "STOPPED"
		self.score = 0

	def draw(self):
		self.snake.draw()
		self.food.draw()

	def update(self):
		if self.state != "STOPPED":
			self.snake.update()
			self.check_collision_with_food()
			self.check_collision_with_self()
			self.check_collision_with_edges()

	def check_collision_with_edges(self):
		if self.snake.body[0].x == cell_number or self.snake.body[0].x == -1:
			self.game_over()
		if self.snake.body[0].y == cell_number or self.snake.body[0].y == -1:
			self.game_over()

	def check_collision_with_self(self):
		headless_body = self.snake.body[1:]
		if self.snake.body[0] in headless_body:
			self.game_over()

	def check_collision_with_food(self):
		if self.food.pos == self.snake.body[0]:
			self.food.recreate(self.snake.body)
			self.snake.add_segment = True
			self.score += 1

	def game_over(self):
		self.snake.reset()
		self.food.recreate(self.snake.body)
		self.state = "STOPPED"
		self.score = 0

screen = pygame.display.set_mode((100 + cell_number*cell_size, 100 + cell_number*cell_size))
pygame.display.set_caption("Retro Snake!")
clock = pygame.time.Clock()
food = pygame.image.load('Graphics/food.png').convert_alpha()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 200)
game = GAME()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and game.snake.direction.y != 1:
				game.snake.direction = Vector2(0, -1)
			if event.key == pygame.K_DOWN and game.snake.direction.y != -1:
				game.snake.direction = Vector2(0, 1)
			if event.key == pygame.K_LEFT and game.snake.direction.x != 1:
				game.snake.direction = Vector2(-1, 0)
			if event.key == pygame.K_RIGHT and game.snake.direction.x != -1:
				game.snake.direction = Vector2(1, 0)
			if game.state == "STOPPED":
				game.state = "RUNNING"
		if event.type == SCREEN_UPDATE:
			game.update()
	screen.fill(GREEN)
	title_surface = title_font.render("Retro Snake", True, DARK_GREEN)
	score_surface = title_font.render(str(game.score), True, DARK_GREEN)
	screen.blit(title_surface, (45,10))
	screen.blit(score_surface, (45,cell_number*cell_size + OFFSET + 10))
	pygame.draw.rect(screen, DARK_GREEN, (45, 45, cell_size*cell_number + 10, cell_size*cell_number + 10), 5)
	game.draw()

	pygame.display.update()
	clock.tick(60)