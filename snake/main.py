import pygame 
import sys
from Snake.constants import WIDTH, HEIGHT, GREEN
from Snake.body import Snake, Segment, Apple

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))

running = True
apple = Apple() 

snake = Snake()
seg = Segment()
seg.add(snake)
seg = Segment(400 + 30,400 )
seg.add(snake)
window.fill((0,0,0))

FPS = 10
clock = pygame.time.Clock()

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      
  window.fill((0,0,0))
  
  snake.drawSquare(apple.x, apple.y, window, GREEN)
  
  snake.move()
  snake.update()
  
  snake.drawSnake(window, seg)
  snake.ifPickedFruit(apple, window)
  
  
  if snake.bodyCollision() or snake.collision2():
    break
    
  pygame.display.flip() # aktualizuj okno 
  
  clock.tick(FPS)
  
pygame.quit()
sys.exit()