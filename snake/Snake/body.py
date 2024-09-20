import pygame
from random import randint
from Snake.constants import RED, SIZE, SIZE2, WIDTH, GREEN, BLACK, HEIGHT

# {0:[], 1:[], 2:[]}

class Apple:
    def __init__(self):
        self.len = WIDTH // SIZE2
        self.x = randint(0, self.len - 1) * SIZE2
        self.y = randint(0, self.len - 1) * SIZE2
        
    

class Segment:
  
  def add(self, snake):
    snake.cor.append(self)
    snake.count += 1
  def __init__(self, x = 420, y = 420):
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
    
  def ifPickedFruit(self, apple, window):
        if apple.x == self.cor[0].x and apple.y == self.cor[0].y:
            self.buildSnake()
            self.drawSquare(apple.x, apple.y, window, BLACK)
            apple.generate_new()
    
  def generateApple(self,apple, window):
    apple.x = randint(0,apple.len) * SIZE2
    apple.y = randint(0,apple.len) * SIZE2
    
    
  def buildSnake(self):
    head = self.cor[0]
    if self.cor[-1].y == self.cor[-2].y:
        if self.cor[-1].x - SIZE != self.cor[-2].x:
            new_segment = Segment(self.cor[-1].x - SIZE, self.cor[-1].y)
            self.cor.append(new_segment)
        if self.cor[-1].x + SIZE != self.cor[-2].x:
            new_segment = Segment(self.cor[-1].x + SIZE, self.cor[-1].y)
            self.cor.append(new_segment)
    if self.cor[-1].x == self.cor[-2].x:
        if self.cor[-1].y - SIZE != self.cor[-2].y:
            new_segment = Segment(self.cor[-1].x, self.cor[-1].y - SIZE)
            self.cor.append(new_segment)
        if self.cor[-1].y + SIZE != self.cor[-2].y:
            new_segment = Segment(self.cor[-1].x, self.cor[-1].y + SIZE)
            self.cor.append(new_segment)

  
  def ifPickedFruit(self, apple, window):
    if apple.x == self.cor[0].x and apple.y == self.cor[0].y:
      self.buildSnake()
      self.drawSquare(apple.x, apple.y, window, BLACK)
      self.generateApple(apple, window)
      
  def bodyCollision(self):
    if len(self.cor) == 2 or len(self.cor) == 1 or len(self.cor) == 0:
      return False
    for a in self.cor[1:]:
      if self.cor[0].x == a.x and self.cor[0].y == a.y:
        return True
    return False
  
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
  
  def move(self):
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
      
  
  def drawSnake(self, window, seg):
    for obj in self.cor:
      #pygame.draw.rect(window, RED, ( obj.x, obj.y, SIZE, SIZE) )
      self.drawSquare(obj.x, obj.y, window, RED)
      
  
  def drawSquare(self, x, y, window, color):
    pygame.draw.rect(window, color, ( x, y, SIZE, SIZE) )
  
  
    