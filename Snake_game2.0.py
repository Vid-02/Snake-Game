import random
import pygame
# global COUNT

class Point:

  #Two Properties X and Y
  def __init__(self, x, y):
    self.x, self.y = x, y
# Override Add and Equal Operators
  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def __eq__(self, other):
    return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y

#Creating Basic Snake Head
class Square:
  #Size Constants
  SQUARE_BORDER_WIDTH = 2
  SQUARE_SIDE_LENGTH = 20
  SQUARE_TOTAL_SIDE_LENGTH = SQUARE_SIDE_LENGTH + SQUARE_BORDER_WIDTH * 2
  

  # We Assign The Color and Position Properties 
  def __init__(self, color, position):
    self.__color = color
    self.position = position

  # Override Eq and Give Position Properties to it
  def __eq__(self, other):
    return self.__class__ == other.__class__ and self.position == other.position

  # Draws On The Surface
  def draw(self, surface):
    #Rectangle Drawing Function
    pygame.draw.rect(surface, self.__color, (
      self.position.x * self.SQUARE_TOTAL_SIDE_LENGTH + self.SQUARE_BORDER_WIDTH,
      self.position.y * self.SQUARE_TOTAL_SIDE_LENGTH + self.SQUARE_BORDER_WIDTH,
      self.SQUARE_SIDE_LENGTH,
      self.SQUARE_SIDE_LENGTH
    ))

#Snake Movements And Variables
class Snake:
  # Constants
  COLOR = 'white'
  COUNT = 0
  DIRECTIONS = {
    pygame.K_UP: {'name': 'up', 'movement': Point(0, -1), 'opposite': 'down'},
    pygame.K_RIGHT: {'name': 'right', 'movement': Point(1, 0), 'opposite': 'left'},
    pygame.K_DOWN: {'name': 'down', 'movement': Point(0, 1), 'opposite': 'up'},
    pygame.K_LEFT: {'name': 'left', 'movement': Point(-1, 0), 'opposite': 'right'}
  }

  # Set Snake to Alive and Keep it Moving in Right
  def __init__(self, position, direction='right'):
    self.__squares = [Square(self.COLOR, position)]
    self.__direction = self.DIRECTIONS[pygame.K_RIGHT]
    self.is_alive = True

  #We Change The Direction on the basis opf pressed key if it is not the Opposite of the current direction
  def move(self, key):
    if (key in self.DIRECTIONS and self.DIRECTIONS[key]['name'] != self.__direction['opposite']):
      self.__direction = self.DIRECTIONS[key]

  # New Square is Represented and Movement is added to it i.e it represents movement
  # We override add to avoid lengthy logic
    new_square = Square(self.COLOR, self.__squares[-1].position + self.__direction['movement'])
    

    #Kill Snake if Out Of Bound
    if (new_square in self.__squares or
    new_square.position.x < 0 or new_square.position.x >= Game.WIDTH or
    new_square.position.y < 0 or new_square.position.y >= Game.HEIGHT):
      self.is_alive = False

    self.__squares.append(new_square)

    return new_square.position

  #Removes The Snakes Tail
  def shrink(self):
    self.__squares.pop(0)

  #Draws all The Squares in The Array
  def draw(self, surface):
    for square in self.__squares:
      square.draw(surface)

#Game Settings
class Game:
  
  # Constants And Size Of Screen
  BACKGROUND_COLOR = 'black'
  FOOD_COLOR = 'red'
  HEIGHT = 30
  WIDTH = 40
  SCREEN_HEIGHT = HEIGHT * Square.SQUARE_TOTAL_SIDE_LENGTH
  SCREEN_WIDTH = WIDTH * Square.SQUARE_TOTAL_SIDE_LENGTH
  COUNT = -1

  #Sets Windows Size and Title__And Calls Reset Method+
  def __init__(self):
    self.__screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    pygame.display.set_caption("OOP Project: Snake Game")

    pygame.font.init()
    self.__font = pygame.font.Font(pygame.font.get_default_font(), 60)

    self.__clock = pygame.time.Clock()
    self.__reset()

  #It is the Only Public Method in the game Class

#Runs in Infinite Loop, Sets the Speed and Frame rate
  def run(self):
    
    while True:
      pygame.time.delay(120)#pause the program for an amount of time
      self.__clock.tick(120) #Frames Per Second

      #Three Methods Are Called
      self.__handle_events() #Checks all the events
      self.__tick()
      self.__draw()

  # Resets Snake Direction and Position
  def __reset(self):
    self.__direction_key = None
    self.__snake = Snake(Point(self.WIDTH / 2, self.HEIGHT / 2))
    self.__generate_food()
    self.COUNT=0

  # Generate random squares on the screen
  def __generate_food(self):
    self.__food = Square(self.FOOD_COLOR, Point(random.randrange(0, self.WIDTH), random.randrange(0, self.HEIGHT)))
    self.COUNT+=1
    self.high=self.COUNT
    print(self.COUNT)
    if self.COUNT>self.high:
      self.high+=1
      print(self.high)

   

  #Checks all the events
  def __handle_events(self):
    #Checks all the events, If Event has quit then Application is ended 
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      #Checks Valid Direction Key
      elif event.type == pygame.KEYDOWN:
        if self.__snake.is_alive and event.key in Snake.DIRECTIONS:
          self.__direction_key = event.key #Assigned to the variable
        #If Snake is dead and user presses space bar it resets
        elif not self.__snake.is_alive and event.key == pygame.K_SPACE:
          self.__reset()

  #Calls Snakes Move Method and Generate Food
  def __tick(self):
    if self.__snake.is_alive:
      #Snake at Food
      if self.__snake.move(self.__direction_key) == self.__food.position:
        self.__generate_food()
      #Snake Not at Food
      else:
        #stops it from growing
        self.__snake.shrink()
  
  # Basic Game Look Before and After D-eath
  def __draw(self):
    self.__screen.fill(self.BACKGROUND_COLOR)
    if self.__snake.is_alive:
      #it keeps drawing food and screen until snake dies
      self.__snake.draw(self.__screen)
      self.__food.draw(self.__screen)
    else:
      #Executes after the snake dies
      text_label = self.__font.render("Press Space To Restart", 1, 'yellow')
      self.__screen.blit(text_label, (self.SCREEN_WIDTH / 2 - text_label.get_width() / 2, 500))
      score_txt = "Score : " + str(self.COUNT*10)
      score_txt1= "High Score :" + str(self.high*10)
      text_label2= self.__font.render(score_txt,True,'red')
      self.__screen.blit(text_label2, (self.SCREEN_WIDTH /2 - text_label.get_width() / 2, 200))
      text_label3= self.__font.render(score_txt1,True,'red')
      self.__screen.blit(text_label3, (self.SCREEN_WIDTH /2 - text_label.get_width() / 2, 300))
      
      with open("score.txt", "w") as file:
        file.write(score_txt)
        file.write("\n")
        file.write(score_txt1)
        

     
    pygame.display.update()
    
Game().run()
