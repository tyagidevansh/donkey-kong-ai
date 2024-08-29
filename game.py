import pygame

gameMap = [
  [100, 260, 700, 40],
  [0, 360, 800, 40]
]
class Player:
  #screen = None
  def __init__(self, screen, left, top, width, height):
    self.screen = screen
    self.playerRect = pygame.Rect(left, top, width, height)
   
  def draw(self):
     pygame.draw.rect(self.screen, "red", self.playerRect) 

  def gravity(self):
    self.playerRect.move_ip(0, 1)
class Map:
  def __init__(self, screen):
    self.screen = screen
    
  def draw(self):
    for platform in gameMap:
      pygame.draw.rect(self.screen, "white", pygame.Rect(platform[0], platform[1], platform[2], platform[3]))
        

def main():
  pygame.init()
  screen = pygame.display.set_mode((800, 400))
  clock = pygame.time.Clock()
  running = True
  dt = 0

  player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
  
  player = Player(screen, 100, 100, 50, 50)  
  map = Map(screen)
  
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        
    screen.fill((0, 0, 0))
    
    player.gravity()
    player.draw()
    map.draw()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
      player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
      player_pos.y += 300 * dt
    if keys[pygame.K_a]:
      player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
      player_pos.x  += 300 * dt
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000 # delta time is seconds since last frame, so frame rate remains 60

  pygame.quit()
  
if __name__ == "__main__":
  main()