import pygame

screenHeight = 400
screenWidth = 800
playerLeft, playerTop, playerWidth, playerHeight = 100, 100, 30, 60


gameMap = [
  #left, top, width, height
  [0, 380, 500, 20],
  [500, 375, 300, 25]
]
class Player: 
  def __init__(self, screen):
    self.screen = screen
    self.playerRect = pygame.Rect(playerLeft, playerTop, playerWidth, playerHeight)
    self.verticalSpeed = 0
    self.horizontalSpeed = 5
    self.acceleration = 0.3
    self.isLineClipping = False
  
  def draw(self):
     pygame.draw.rect(self.screen, "red", self.playerRect) 

  def gravity(self):
    self.isLineClipping = False
    for platform in gameMap:
      clippedLine = self.playerRect.clipline((platform[0], platform[1]), (platform[0] + platform[2], platform[1]))
      if clippedLine:
        start, end = clippedLine
        self.isLineClipping = True
        self.verticalSpeed = 0
        x1, y1 = start
        self.playerRect.update(playerLeft, y1 - playerHeight, playerWidth, playerHeight)
    
    if not self.isLineClipping:  
      self.verticalSpeed += self.acceleration
      self.playerRect.move_ip(0, self.verticalSpeed)
      
  def jump(self):
    if (self.isLineClipping):
      self.verticalSpeed = -7
    while self.verticalSpeed < 0:
      self.playerRect.move_ip(0, self.verticalSpeed)
      self.verticalSpeed += self.acceleration
      self.hasJumped = False
  
  def moveLeft(self):
    self.playerRect.move_ip(-self.horizontalSpeed, 0) 
    
class Map:
  def __init__(self, screen):
    self.screen = screen
    
  def draw(self):
    for platform in gameMap:
      pygame.draw.rect(self.screen, "white", pygame.Rect(platform[0], platform[1], platform[2], platform[3]))
        

def main():
  pygame.init()
  screen = pygame.display.set_mode((screenWidth, screenHeight))
  clock = pygame.time.Clock()
  running = True
  dt = 0

  player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
  
  player = Player(screen)  
  map = Map(screen)
  
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        
    screen.fill((0, 0, 0))
    
    player.gravity()
    
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
      player.jump()
    if keys[pygame.K_s]:
      player_pos.y += 300 * dt
    if keys[pygame.K_LEFT]:
      player.moveLeft()
    if keys[pygame.K_d]:
      player_pos.x  += 300 * dt
    player.draw()
    map.draw()
    pygame.display.flip()
    dt = clock.tick(60) / 1000 # delta time is seconds since last frame, so frame rate remains 60
    
  pygame.quit()
  
if __name__ == "__main__":
  main()