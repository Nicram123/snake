import pygame 
import sys
from Snake.constants import WIDTH, HEIGHT, GREEN
from Snake.body import Snake, Segment, Apple
from tensorflow.keras.models import load_model
import numpy as np
import os 

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))

running = True
apple = Apple() 

snake = Snake()
seg = Segment()
seg.add(snake)
seg = Segment(400 + 30,400 ) # 400 + 30,400
seg.add(snake)
window.fill((0,0,0))
FPS = 40
clock = pygame.time.Clock()

# 100 to goated 
q_network = load_model(r"C:\Users\marci\snake\models\ snake_ai_ep100.keras", compile=False)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill((0, 0, 0))

    # --- RUCH --- (model podejmuje decyzję)
    # Stan przed ruchem:
    diffX = snake.cor[0].x - apple.x
    diffY = snake.cor[0].y - apple.y
    distance_to_food = np.sqrt(diffX**2 + diffY**2)

    dangerList = snake.futureCollision()
    danger_up, danger_down, danger_left, danger_right = dangerList

    dir_up = 1.0 if snake.prev_keys == 'up' else 0.0
    dir_down = 1.0 if snake.prev_keys == 'down' else 0.0
    dir_left = 1.0 if snake.prev_keys == 'left' else 0.0
    dir_right = 1.0 if snake.prev_keys == 'right' else 0.0

    apple_left = 1.0 if diffX > 0 else 0.0
    apple_right = 1.0 if diffX < 0 else 0.0
    apple_up = 1.0 if diffY > 0 else 0.0
    apple_down = 1.0 if diffY < 0 else 0.0

    state = np.array([
        diffX / WIDTH,
        diffY / HEIGHT,
        distance_to_food / np.sqrt(WIDTH**2 + HEIGHT**2),
        danger_up, danger_down, danger_left, danger_right,
        dir_up, dir_down, dir_left, dir_right,
        apple_left, apple_right, apple_up, apple_down
    ], dtype=np.float32)
    state = np.expand_dims(state, axis=0)

    # --- WYBÓR AKCJI ---
    q_values = q_network(state)
    action = np.argmax(q_values[0])

    # --- RUCH WG AKCJI ---
    snake.moveRL(action)
    snake.update()

    # --- SPRAWDZENIE JABŁKA PO AKTUALIZACJI ---
    snake.ifPickedFruit(apple, window)
    
    #snake.update()         # aktualizuj pozycję
    #snake.ifPickedFruit(apple, window)  # zbieranie
    #snake.moveRL(action) 

    # --- RYSOWANIE ---
    snake.drawSquare(apple.x, apple.y, window, GREEN)
    snake.drawSnake(window, seg)
    
    

    # --- KOLIZJE ---
    if snake.bodyCollision() or snake.collision2():
        break

    pygame.display.flip()
    clock.tick(FPS)

  
pygame.quit()
sys.exit()