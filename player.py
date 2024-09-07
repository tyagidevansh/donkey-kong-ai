import pygame
import math
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
        self.player_area = self.playerRect.width * self.playerRect.height       
        self.isImageFacingLeft = False
        self.gameWon = False
        self.framesSinceSwitch = 0
        self.framesSinceSwitchClimb = 0
        self.verticalSpeed = 0
        self.horizontalSpeed = 200
        self.acceleration = 15
        self.jumpSpeed = -7500
        self.isJumping = False
        self.isLineClipping = False
        self.isClimbing = False
        self.isNearLadder = False
        self.isMoving = False
        self.score = 0

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

        if self.playerRect.left < peachPos[1] + 90 and self.playerRect.bottom <= peachPos[0]:
            self.score += 1000
            self.gameWon = True
            print("victory")
        
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
        detection_zone = pygame.Rect(self.playerRect.left + 5, self.playerRect.bottom, self.playerRect.width - 20, 7)
        
        for ladder in ladders:
            intersection = self.playerRect.clip(ladder)
            ladder_below = detection_zone.colliderect(ladder)
            
            intersection_area = intersection.width * intersection.height
            if intersection_area >= 0.55 * self.player_area or ladder_below:
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
        for ladder in ladders:
            if (not self.playerRect.colliderect(ladder)):
                self.isNearLadder = False
                if self.isClimbing:    
                    self.isClimbing = False
            else:
                self.isNearLadder = True   
        
        if (not self.isImageFacingLeft):
            self.imageStand = pygame.transform.flip(self.imageStand, True, False) 
            self.imageRun = pygame.transform.flip(self.imageRun, True, False)
            self.imageJump = pygame.transform.flip(self.imageJump, True, False)
            self.isImageFacingLeft = True
            
        if self.playerRect.left - self.horizontalSpeed * dt > 2:
            self.playerRect.move_ip(-self.horizontalSpeed * dt, 0)
        
    def moveRight(self, ladders, dt):
        self.isMoving = True
        for ladder in ladders:
            if (not self.playerRect.colliderect(ladder)):
                self.isNearLadder = False
                if self.isClimbing:    
                    self.isClimbing = False
            else:
                self.isNearLadder = True    

        if (self.isImageFacingLeft):
            self.imageStand = pygame.transform.flip(self.imageStand, True, False) 
            self.imageRun = pygame.transform.flip(self.imageRun, True, False)
            self.imageJump = pygame.transform.flip(self.imageJump, True, False)
            self.isImageFacingLeft = False
                    
        if self.playerRect.right + self.horizontalSpeed * dt < window_width - 2:
            self.playerRect.move_ip(self.horizontalSpeed * dt, 0)
    
    def checkBarrelCollision(self, barrels):
        for barrel in barrels:
            intersection = self.playerRect.clip(barrel.barrelRect)
            intersection_area = intersection.width * intersection.height
            if 0 < intersection_area < 0.3 * self.player_area:
                self.score += 20
            if intersection_area >= 0.33 * self.player_area:
                #print("collision!!")
                return True
        
        return False   

    def nearestBarrels(self, barrels):
        nearest = []
        for barrel in barrels:
            p = self.playerRect.center
            b = barrel.barrelRect.center
            
            distance = math.sqrt((b[0] - p[0]) ** 2 + (b[1] - p[1]) ** 2)
            nearest.append([distance, b[0], b[1]])
            
        nearest.sort(key = lambda x:x[0])
        
        while len(nearest) < 5:
            nearest.append([0, 0, 0])
        
        return nearest[:5]

    def reset(self):
        self.playerRect.left = 150
        self.playerRect.top = screen_height - 200
        if not self.gameWon:
            self.score = 0
        else:
            self.gameWon = False
        #self.isImageFacingLeft = False