import random
import pygame
from settings import *

class Barrel(pygame.sprite.Sprite):
  def __init__(self, screen, platforms, ladders, x, y):
    super().__init__()
    self.screen = screen
    self.platforms = platforms
    self.ladders = ladders
    self.barrel = barrel_img1
    #self.barrel = pygame.transform.scale(self.barrel, (playerWidth, playerHeight))
    self.barrelRect = self.barrel.get_rect()
    self.barrelRect.left = x
    self.barrelRect.bottom = y
    self.isMovingLeft = False
    self.isClimbing = False
    self.currentLadder = None
    self.speed = 200
    self.isLineClipping = False
    self.isAlive = True
  
  def update(self, dt):
    if not self.isClimbing:
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

      if self.barrelRect.left <= barrelX + 100 and self.barrelRect.bottom > barrelY:
        self.isAlive = False  
      
    self.climbDown(dt)

  def gravity(self, dt):
    self.isLineClipping = False
    for platform in self.platforms:
      if self.barrelRect.colliderect(platform):
        self.isLineClipping = True
        break

    if not self.isLineClipping:
      self.barrelRect.bottom += self.speed * dt / 2       

  def climbDown(self, dt):
    detectionZone = pygame.Rect(self.barrelRect.left + 15, self.barrelRect.bottom, self.barrelRect.width - 20, 7)
    #pygame.draw.rect(self.screen, (0, 0, 255), detectionZone)
    if not self.isClimbing: 
      for ladder in self.ladders:
        ladderBelow = detectionZone.colliderect(ladder)
        if ladderBelow:
            if random.randint(0, 1000) > 900:  
              self.isClimbing = True
              self.isMovingLeft = not self.isMovingLeft
              self.currentLadder = ladder
              self.barrel = barrel_side
              break
    
    if self.isClimbing and self.currentLadder is not None:
      self.barrelRect.top += self.speed * dt / 1.2

      if not detectionZone.colliderect(self.currentLadder):
        self.barrelRect.bottom -= 5
        self.barrel = barrel_img1
        self.isClimbing = False
        self.currentLadder = None
        
  def draw(self):
    self.screen.blit(self.barrel, self.barrelRect)