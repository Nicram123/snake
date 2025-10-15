import pygame
from random import randint
from Snake.constants import RED, SIZE, SIZE2, WIDTH, GREEN, BLACK, HEIGHT  # Snake.
from copy import deepcopy 

# {0:[], 1:[], 2:[]}

class Apple:
    def __init__(self):
        self.len = WIDTH // SIZE2  # 800 // 35 
        self.x = randint(0, self.len-1) * SIZE2
        self.y = randint(0, self.len-1) * SIZE2
        
    

class Segment:
  
  def add(self, snake):
    snake.cor.append(self)
    snake.count += 1
  def __init__(self, x = 440, y = 440): # 424 424 
    self.x = x
    self.y = y
    
class Snake:
  def __init__(self):
    self.cor = []
    self.count = 1
    
    self.a = 0
    self.b = 0
    
    self.keys = None
    self.prev_keys = None
   
  # jesli owoc zostal zebrany  
  def ifPickedFruit(self, apple, window):
        if apple.x == self.cor[0].x and apple.y == self.cor[0].y:
            # dodaje segment do tablicy self.cor 
            self.buildSnake()
            # zakrywa owoc który został zebrany 
            self.drawSquare(apple.x, apple.y, window, BLACK)
            # generuje nowy owoc 
            apple.generate_new()
  # generuj owoc   
  def generateApple(self,apple):
    apple.x = randint(0,apple.len-1) * SIZE2
    apple.y = randint(0,apple.len-1) * SIZE2
    
  # dodaj segment obiekt do tablicy self.cor w roznych polozeniach węża 
  def buildSnake(self):
    head = self.cor[0]
    # poziome ułożenie węża 
    if self.cor[-1].y == self.cor[-2].y:
        if self.cor[-1].x - SIZE != self.cor[-2].x:
            new_segment = Segment(self.cor[-1].x - SIZE, self.cor[-1].y)
            self.cor.append(new_segment)
        if self.cor[-1].x + SIZE != self.cor[-2].x:
            new_segment = Segment(self.cor[-1].x + SIZE, self.cor[-1].y)
            self.cor.append(new_segment)
    # pionowe ułozenie węża 
    if self.cor[-1].x == self.cor[-2].x:
        if self.cor[-1].y - SIZE != self.cor[-2].y:
            new_segment = Segment(self.cor[-1].x, self.cor[-1].y - SIZE)
            self.cor.append(new_segment)
        if self.cor[-1].y + SIZE != self.cor[-2].y:
            new_segment = Segment(self.cor[-1].x, self.cor[-1].y + SIZE)
            self.cor.append(new_segment)

  # jesli owoc zostal zebrany  
  def ifPickedFruit(self, apple, window):
    # jesli head pokrywa się z fruit
    if apple.x == self.cor[0].x and apple.y == self.cor[0].y: 
      # dodaje segment do tablicy  
      self.buildSnake() 
      # w miejscu zebranego owoca zamaż to pole 
      self.drawSquare(apple.x, apple.y, window, BLACK) 
      # wygeneruj nowy owoc 
      self.generateApple(apple)
      
  def ifPickedFruitRL(self, apple):
    # jesli head pokrywa się z fruit
    if apple.x == self.cor[0].x and apple.y == self.cor[0].y: 
      # dodaje segment do tablicy  
      self.buildSnake() 
      # wygeneruj nowy owoc 
      self.generateApple(apple)
      
      return True 
    return False 
  
  # kolizja węża    
  def bodyCollision(self): 
    # wtedy nie dochodz do kolizji 
    if len(self.cor) == 2 or len(self.cor) == 1 or len(self.cor) == 0:
      return False
    # pobieramy wszystkie oprocz heada 
    for a in self.cor[1:]:
      # colizia heada z jakimkolwiek przyczynkiem w ciele 
      if self.cor[0].x == a.x and self.cor[0].y == a.y:
        return True
    return False
  
  # kolizja ze sciana 
  def collision2(self):
    if self.cor[0].x < 0:
        return True
    elif self.cor[0].x >= WIDTH:
        return True
    elif self.cor[0].y < 0:
        return True
    elif self.cor[0].y >= HEIGHT:
        return True
    return False
      
  def collision(self):
    if self.cor[0].x < 0:
        self.cor[0].x = WIDTH - SIZE
    elif self.cor[0].x >= WIDTH:
        self.cor[0].x = 0
    elif self.cor[0].y < 0:
        self.cor[0].y = WIDTH - SIZE
    elif self.cor[0].y >= HEIGHT:
        self.cor[0].y = 0

  # nie mozna skrecac wężem jeśli chcemy `gwaltownie zmienic kierunek` o 180 stopni 
  def IfTurnBackInOppositeDirect(self):
    if self.keys[pygame.K_LEFT]:
      if self.prev_keys == 'right':
        return False
    if self.keys[pygame.K_RIGHT]:
      if self.prev_keys == 'left':
        return False
    if self.keys[pygame.K_UP]:
      if self.prev_keys == 'down':
        return False
    if self.keys[pygame.K_DOWN]:
      if self.prev_keys == 'up':
        return False
    return True
  
  def IfTurnBackInOppositeDirectRL(self, action):
    if action == 0: # up 
      if self.prev_keys == 'down':
        return False
    if action == 1: # down 
      if self.prev_keys == 'up':
        return False
    if action == 2: # left 
      if self.prev_keys == 'right':
        return False
    if action == 3: # right 
      if self.prev_keys == 'left':
        return False
    return True
  
  def futureCollision(self):
    # returns [danger_up, danger_down, danger_left, danger_right]
    dangerousMove = [0,0,0,0]
    for action_idx in range(4):
        snakeTemp = deepcopy(self)
        # jeśli ruch jest zakazany (skręt o 180), oznacz jako niebezpieczny
        if not snakeTemp.IfTurnBackInOppositeDirectRL(action_idx):
            dangerousMove[action_idx] = 1
            continue
        snakeTemp.moveRL(action_idx)
        snakeTemp.update()
        if snakeTemp.bodyCollision() or snakeTemp.collision2():
            dangerousMove[action_idx] = 1
    return dangerousMove

  
        
  def move(self):
    # [left right up down],  [TRUE FALSE FALSE FALSE]  jesli left wciśnięty 
    self.keys = pygame.key.get_pressed()
    if self.IfTurnBackInOppositeDirect() and self.keys[pygame.K_LEFT]:
      self.prev_keys = 'left'
      self.a, self.b = -SIZE, 0
      #print("siema")
    if self.IfTurnBackInOppositeDirect() and self.keys[pygame.K_RIGHT]:
      self.prev_keys = 'right'
      self.a, self.b = SIZE, 0
    if self.IfTurnBackInOppositeDirect() and self.keys[pygame.K_UP]:
      self.prev_keys = 'up'
      self.a, self.b = 0, -SIZE
    if self.IfTurnBackInOppositeDirect() and self.keys[pygame.K_DOWN]:
      self.prev_keys = 'down'
      self.a, self.b = 0, SIZE
      
  def moveRL(self, action):
    if self.IfTurnBackInOppositeDirectRL(action) and action == 0: # up
      self.prev_keys = 'up'
      self.a, self.b = 0, -SIZE
      #print("siema")
    if self.IfTurnBackInOppositeDirectRL(action) and action == 1: # down 
      self.prev_keys = 'down'
      self.a, self.b = 0, SIZE
    if self.IfTurnBackInOppositeDirectRL(action) and action == 2: # left 
      self.prev_keys = 'left'
      self.a, self.b = -SIZE, 0
    if self.IfTurnBackInOppositeDirectRL(action) and action == 3: # right 
      self.prev_keys = 'right'
      self.a, self.b = SIZE, 0
      
  # ukladanie segmentów przy przemieszczaniu się węża 
  def update(self):
    tempX, tempY = self.cor[0].x, self.cor[0].y
    tempX_, tempY_ = 0, 0
    self.cor[0].x, self.cor[0].y = self.cor[0].x + self.a, self.cor[0].y + self.b
    for ix, obj in enumerate(self.cor[1:]):
      if ix == 0:
        tempX_, tempY_ = obj.x, obj.y
        obj.x, obj.y = tempX, tempY
        continue 
      tempX2_, tempY2_ = obj.x, obj.y
      obj.x, obj.y = tempX_, tempY_
      tempX_, tempY_ = tempX2_, tempY2_
      
  
  # każdy segment osobno rysuje  
  def drawSnake(self, window, seg):
    for obj in self.cor:
      #pygame.draw.rect(window, RED, ( obj.x, obj.y, SIZE, SIZE) )
      self.drawSquare(obj.x, obj.y, window, RED)
      
  
  # rysuje kwadrat segment węża 
  def drawSquare(self, x, y, window, color):
    pygame.draw.rect(window, color, ( x, y, SIZE, SIZE) )
  
  
    