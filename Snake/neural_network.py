import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input
from Snake.constants import WIDTH, HEIGHT, SIZE2
from random import randint
import numpy as np  
from Snake.body import Apple, Segment, Snake 
from collections import deque


class SnakeEnv:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        self.reset()
        
    

    def reset(self):
        # Pozycje paletek i piłki
        seg = Segment() 
        apple = Apple() 
        snake = Snake() 
        
        seg.add(snake)
        seg = Segment(400 + 25,400 ) # (400 + 30,400
        seg.add(snake)  
        
        self.recent_heads = deque(maxlen=40)
        self.x = snake.cor[0].x
        self.y = snake.cor[0].y 
        self.len = WIDTH // SIZE2  # 800 // 35 
        self.fruitX = apple.x # randint(0, self.len - 1) * SIZE2 
        self.fruitY = apple.y # randint(0, self.len - 1) * SIZE2 
        self.diffX = self.x - self.fruitX 
        self.diffY = self.y - self.fruitY 
        self.distance_to_food = np.sqrt(self.diffX**2 + self.diffY**2)
        self.danger_up = 0 # nie zderzy 
        self.danger_down = 0 
        self.danger_left = 0 
        self.danger_right = 0 
        
        self.dir_up = 0
        self.dir_down = 0
        self.dir_left = 0
        self.dir_right = 0
        
        self.apple_left = 1.0 if self.diffX > 0 else 0.0
        self.apple_right = 1.0 if self.diffX < 0 else 0.0
        self.apple_up = 1.0 if self.diffY > 0 else 0.0
        self.apple_down = 1.0 if self.diffY < 0 else 0.0

        self.steps_since_food = 0
        
        # Normalizacja 
        state = np.array([
            self.diffX / self.width,
            self.diffY / self.height,
            self.distance_to_food / np.sqrt(self.width**2 + self.height**2),
            self.danger_up,
            self.danger_down,
            self.danger_left,
            self.danger_right, 
            self.dir_up, 
            self.dir_down, 
            self.dir_left, 
            self.dir_right, 
            
            self.apple_left, 
            self.apple_right, 
            self.apple_up, 
            self.apple_down
        ], dtype=np.float32)
        return state, snake, apple

    def step(self, action, snake, apple):
        # self.direction = [1, 0, 0, 0] # up down left right  
        reward = 0 
        done = False 
        
        snake.moveRL(action) 
        snake.update() 
        flag = snake.ifPickedFruitRL(apple)
        
        self.fruitX = apple.x  
        self.fruitY = apple.y 
        
        self.diffX = snake.cor[0].x - self.fruitX 
        self.diffY = snake.cor[0].y - self.fruitY 
        self.distance_to_food = np.sqrt(self.diffX**2 + self.diffY**2)
        
        dangerList = snake.futureCollision() 
        self.danger_up = dangerList[0] 
        self.danger_down = dangerList[1]
        self.danger_left = dangerList[2]
        self.danger_right = dangerList[3]
         
         
        self.dir_up = 1.0 if snake.prev_keys == 'up' else 0.0
        self.dir_down = 1.0 if snake.prev_keys == 'down' else 0.0
        self.dir_left = 1.0 if snake.prev_keys == 'left' else 0.0
        self.dir_right = 1.0 if snake.prev_keys == 'right' else 0.0 
        
        self.apple_left = 1.0 if self.diffX > 0 else 0.0
        self.apple_right = 1.0 if self.diffX < 0 else 0.0
        self.apple_up = 1.0 if self.diffY > 0 else 0.0
        self.apple_down = 1.0 if self.diffY < 0 else 0.0

        
        self.prev_distance_to_food = getattr(self, 'prev_distance_to_food', self.distance_to_food)
        #self.steps_since_food += 1
        #head_pos = (snake.cor[0].x, snake.cor[0].y)
        #if head_pos in self.recent_heads:
        #    reward -= 0.5
        #self.recent_heads.append(head_pos)
        
        if flag: 
          reward += 10 # 10
          #self.steps_since_food = 0
        reward -= 0.01 
        
        if self.distance_to_food < self.prev_distance_to_food:
            reward += 0.2
        else:
            reward -= 0.1
            
        if snake.bodyCollision() or snake.collision2(): 
          reward -= 10 
          done = True 
          
        #if self.steps_since_food > 150:
        #    reward -= 5.0
        #    done = True
        self.prev_distance_to_food = self.distance_to_food
        
        
        # --- nowy stan ---
        state = np.array([
            self.diffX / self.width,
            self.diffY / self.height,
            self.distance_to_food / np.sqrt(self.width**2 + self.height**2),
            self.danger_up,
            self.danger_down,
            self.danger_left,
            self.danger_right, 
            self.dir_up, 
            self.dir_down, 
            self.dir_left, 
            self.dir_right, 
            self.apple_left, 
            self.apple_right, 
            self.apple_up, 
            self.apple_down
        ], dtype=np.float32)
        return state, reward, done 

# --- Sieć Q-learning ---
def build_q_network(state_size=15, num_actions=4):
    model = Sequential([
        Input((state_size,)),
        Dense(128, activation='relu'),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(num_actions)
    ])
    return model
