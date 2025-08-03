"""
🐍 Snake Game – v2.1-Stable

Minimal snake game using Python + pygame.

🎮 Features:
- Arrow keys to move
- Eat red squares to grow
- Wall collision = Game Over
- Toggle wrap mode: W key
- Pause/unpause: P key
- Set speed: 1 = slow, 2 = normal, 3 = fast
- UI shows score, speed, wrap mode, pause

🔁 Controls:
- Arrow keys: move
- W: toggle wall wrap
- P: pause/resume
- 1/2/3: change game speed
- R: restart after game over
- Q: quit after game over

🛠 Requirements:
- Python 3.x
- pygame (pip install pygame)

▶️ Run:
    python snake.py

"""

import pygame, random, sys

pygame.init()
W, H, SIZE = 600, 400, 20
win = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

snake = [(5, 5)]
dx, dy = 1, 0
food = (10, 10)
score = 0
wrap = False
paused = False
speed = 10

def draw():
	win.fill((0, 0, 0))
	for x, y in snake:
		pygame.draw.rect(win, (0, 255, 0), (x*SIZE, y*SIZE, SIZE-1, SIZE-1))
	fx, fy = food
	pygame.draw.rect(win, (255, 0, 0), (fx*SIZE, fy*SIZE, SIZE-1, SIZE-1))
	txt = font.render(f"Score: {score}  Speed: {speed}  {'Wrap' if wrap else 'NoWrap'}", True, (255,255,255))
	win.blit(txt, (10, 10))
	if paused:
		pause_txt = font.render("PAUSED", True, (255,255,0))
		win.blit(pause_txt, (W//2 - 50, H//2))
	pygame.display.flip()

def move():
	global snake, food, score
	head = (snake[0][0] + dx, snake[0][1] + dy)
	if wrap:
		head = (head[0] % (W//SIZE), head[1] % (H//SIZE))
	elif (head in snake or head[0] < 0 or head[0] >= W//SIZE or head[1] < 0 or head[1] >= H//SIZE):
		game_over()
	if head in snake:
		game_over()
	snake.insert(0, head)
	if head == food:
		score += 1
		while True:
			food = (random.randint(0, W//SIZE-1), random.randint(0, H//SIZE-1))
			if food not in snake: break
		globals()['food'] = food
	else:
		snake.pop()

def game_over():
	txt = font.render("Game Over - R to Restart or Q to Quit", True, (255, 255, 255))
	win.blit(txt, (W//2 - 180, H//2))
	pygame.display.flip()
	pygame.time.wait(1000)
	wait()

def wait():
	while True:
		handle_events(waiting=True)
		clock.tick(10)

def reset():
	global snake, dx, dy, food, score, paused
	snake = [(5, 5)]
	dx, dy = 1, 0
	food = (10, 10)
	score = 0
	paused = False

def handle_events(waiting=False):
	global dx, dy, wrap, paused, speed
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if e.type == pygame.KEYDOWN:
			if waiting:
				if e.key == pygame.K_r: reset(); return
				if e.key == pygame.K_q: pygame.quit(); sys.exit()
			else:
				if e.key == pygame.K_UP and dy == 0: dx, dy = 0, -1
				if e.key == pygame.K_DOWN and dy == 0: dx, dy = 0, 1
				if e.key == pygame.K_LEFT and dx == 0: dx, dy = -1, 0
				if e.key == pygame.K_RIGHT and dx == 0: dx, dy = 1, 0
				if e.key == pygame.K_w: wrap = not wrap
				if e.key == pygame.K_p: paused = not paused
				if e.key == pygame.K_1: speed = 5
				if e.key == pygame.K_2: speed = 10
				if e.key == pygame.K_3: speed = 15

while True:
	handle_events()
	if not paused:
		move()
		draw()
	clock.tick(speed)
