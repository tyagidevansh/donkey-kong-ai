import pygame
from settings import *

class Barrel(pygame.sprite.Sprite):
  def __init__(self, screen, platforms, ladders, x, y):
    super().__init__()
    self.screen = screen
    self.platforms = platforms
    self.ladders = ladders
    self.barrelSide = barrel_img1
    self.barrelSide = pygame.transform.scale(self.barrelSide, (playerWidth, playerHeight))
    self.barrelRect = self.barrelSide.get_rect()
    self.barrelRect.left = x
    self.barrelRect.bottom = y
    self.isMovingLeft = False
    self.nearLadder = False
    self.isClimbing = False
    self.speed = 200
    self.isLineClipping = False
    self.isAlive = True
   
  def update(self, dt):
    if not isClimbing:
      if self.isMovingLeft:
        self.barrelRect.left -= self.speed * dt
        if self.barrelRect.left < 0:
          self.isMovingLeft = False
          self.barrelRect.bottom += 10
          self.barrelRect.left += 10
      else:
        self.barrelRect.left += self.speed * dt 
        if self.barrelRect.right > window_width:
          self.isMovingLeft = True
          self.barrelRect.bottom += 20
          self.barrelRect.left -= 10       
      self.gravity(dt)     
      
      if self.barrelRect.right <= barrelX and self.barrelRect.bottom > barrelY:
        self.isAlive = False        

  def gravity(self, dt):
    self.isLineClipping = False
    for platform in self.platforms:
      if self.isLineClipping: break
      if self.barrelRect.colliderect(platform):
        self.isLineClipping = True
    
    if not self.isLineClipping:
      self.barrelRect.bottom += self.speed * dt / 2       
  
  def draw(self):
    screen.blit(self.barrelSide, self.barrelRect)