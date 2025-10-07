# test_state_consistency.py
from neural_network import SnakeEnv
import numpy as np

env = SnakeEnv()
state_env, snake, apple = env.reset()

# buduj "main-style" state z obiektu snake/apple
diffX = snake.cor[0].x - apple.x
diffY = snake.cor[0].y - apple.y
distance_to_food = np.sqrt(diffX**2 + diffY**2)
danger = snake.futureCollision()
dir_up = 1.0 if snake.prev_keys == 'up' else 0.0
dir_down = 1.0 if snake.prev_keys == 'down' else 0.0
dir_left = 1.0 if snake.prev_keys == 'left' else 0.0
dir_right = 1.0 if snake.prev_keys == 'right' else 0.0

apple_left = 1.0 if diffX > 0 else 0.0
apple_right = 1.0 if diffX < 0 else 0.0
apple_up = 1.0 if diffY > 0 else 0.0
apple_down = 1.0 if diffY < 0 else 0.0

state_main = np.array([
    diffX / env.width, diffY / env.height,
    distance_to_food / np.sqrt(env.width**2 + env.height**2),
    danger[0], danger[1], danger[2], danger[3],
    dir_up, dir_down, dir_left, dir_right,
    apple_left, apple_right, apple_up, apple_down
], dtype=np.float32)

print("state_env:", state_env)
print("state_main:", state_main)
print("Allclose:", np.allclose(state_env, state_main))
