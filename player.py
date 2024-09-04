import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.imageStand = standing
        self.imageStand = pygame.transform.scale(self.imageStand, (playerWidth, playerHeight))
        self.imageRun = running
        self.imageRun = pygame.transform.scale(self.imageRun, (playerWidth, playerHeight))
        self.playerRect = self.imageStand.get_rect()
        self.imageJump = jumping
        self.imageJump = pygame.transform.scale(self.imageJump, (playerWidth, playerHeight))
        #self.playerRectJump = self.imageJump.get_rect()
        self.imageClimb1 = climbing1
        self.imageClimb1 = pygame.transform.scale(self.imageClimb1, (playerWidth, playerHeight))
        self.imageClimb2 = climbing2
        self.imageClimb2 = pygame.transform.scale(self.imageClimb2, (playerWidth, playerHeight))
        self.playerRect.left = 150
        self.playerRect.top = screen_height - 200
        self.isImageFacingLeft = False
        self.framesSinceSwitch = 0
        self.framesSinceSwitchClimb = 0
        self.verticalSpeed = 0
        self.horizontalSpeed = 200
        self.acceleration = 15
        self.jumpSpeed = -7000
        self.isJumping = False
        self.isLineClipping = False
        self.isClimbing = False
        self.isMoving = False

    def draw(self):
        if self.isJumping:
            self.screen.blit(self.imageJump, self.playerRect)
        elif self.isMoving:
            if self.framesSinceSwitch < 4:
                self.screen.blit(self.imageRun, self.playerRect)
            else:
                self.screen.blit(self.imageStand, self.playerRect)

            self.framesSinceSwitch = (self.framesSinceSwitch + 1) % 8
        
        elif self.isClimbing:
            if self.framesSinceSwitchClimb < 4:
                self.screen.blit(self.imageClimb1, self.playerRect)
            else:
                self.screen.blit(self.imageClimb2, self.playerRect)
            self.framesSinceSwitchClimb = (self.framesSinceSwitchClimb + 1) % 8
        else:
            self.screen.blit(self.imageStand, self.playerRect)
            self.framesSinceSwitch = 0  
        
    def gravity(self, platforms, dt):
        if self.isClimbing:  #no gravity when climbing
            return
        self.isLineClipping = False
        for platform in platforms:
            if self.playerRect.colliderect(platform):
                self.isLineClipping = True
                self.verticalSpeed = 0
                self.playerRect.bottom = platform.top
                self.isJumping = False
                break

        if not self.isLineClipping:  
            self.verticalSpeed += self.acceleration
            self.playerRect.move_ip(0, self.verticalSpeed * dt) #the player is jittering but oh well

    def jump(self, dt):
        if not self.isJumping and self.isLineClipping and not self.isClimbing:
            self.isJumping = True
            self.verticalSpeed = self.jumpSpeed * dt

        if self.isJumping:
            self.verticalSpeed += self.acceleration

    def climb(self, ladders, isClimbingUp, dt):
        self.isClimbing = False
        player_area = self.playerRect.width * self.playerRect.height
        for ladder in ladders:
            intersection = self.playerRect.clip(ladder)
            intersection_area = intersection.width * intersection.height
            if intersection_area >= 0.55 * player_area:
                self.isClimbing = True
                if isClimbingUp:
                    self.playerRect.move_ip(0, -self.horizontalSpeed * dt / 2)
                else:
                    self.playerRect.move_ip(0, self.horizontalSpeed * dt / 2)
                self.verticalSpeed = 0
                self.isJumping = False
                break

    def moveLeft(self, ladders, dt):
        self.isMoving = True
        if (self.isClimbing):
            for ladder in ladders:
                if (not self.playerRect.colliderect(ladder)):
                    self.isClimbing = False
        
        if (not self.isImageFacingLeft):
            self.imageStand = pygame.transform.flip(self.imageStand, True, False) 
            self.imageRun = pygame.transform.flip(self.imageRun, True, False)
            self.imageJump = pygame.transform.flip(self.imageJump, True, False)
            self.isImageFacingLeft = True
            
        if self.playerRect.left - self.horizontalSpeed * dt > 2:
            self.playerRect.move_ip(-self.horizontalSpeed * dt, 0)
        
    def moveRight(self, ladders, dt):
        self.isMoving = True
        if (self.isClimbing):
            for ladder in ladders:
                if (not self.playerRect.colliderect(ladder)):
                    self.isClimbing = False

        if (self.isImageFacingLeft):
            self.imageStand = pygame.transform.flip(self.imageStand, True, False) 
            self.imageRun = pygame.transform.flip(self.imageRun, True, False)
            self.imageJump = pygame.transform.flip(self.imageJump, True, False)
            self.isImageFacingLeft = False
                    
        if self.playerRect.right + self.horizontalSpeed * dt < window_width - 2:
            self.playerRect.move_ip(self.horizontalSpeed * dt, 0)
        
