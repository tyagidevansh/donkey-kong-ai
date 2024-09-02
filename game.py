import os
import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1' 
pygame.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
window_width, window_height = screen_width - 800, screen_height - 150
screen = pygame.display.set_mode([window_width, window_height])

pygame.display.set_caption('Donkey Kong')

section_width = window_width // 32
section_height = window_height // 32
slope = section_height // 8

playerWidth, playerHeight = 30, 30

barrel_img = pygame.transform.scale(pygame.image.load('assets/images/barrels/barrel.png'),
                                    (section_width * 1.5, section_height * 2))
flames_img = pygame.transform.scale(pygame.image.load('assets/images/fire.png'),
                                    (section_width * 2, section_height))
barrel_side = pygame.transform.scale(pygame.image.load('assets/images/barrels/barrel2.png'),
                                     (section_width * 2, section_height * 2.5))
dk1 = pygame.transform.scale(pygame.image.load('assets/images/dk/dk1.png'),
                             (section_width * 5, section_height * 5))
dk2 = pygame.transform.scale(pygame.image.load('assets/images/dk/dk2.png'),
                             (section_width * 5, section_height * 5))
dk3 = pygame.transform.scale(pygame.image.load('assets/images/dk/dk3.png'),
                             (section_width * 5, section_height * 5))
peach1 = pygame.transform.scale(pygame.image.load('assets/images/peach/peach1.png'),
                                (2 * section_width, 3 * section_height))
peach2 = pygame.transform.scale(pygame.image.load('assets/images/peach/peach2.png'),
                                (2 * section_width, 3 * section_height))
fireball = pygame.transform.scale(pygame.image.load('assets/images/fireball.png'),
                                  (1.5 * section_width, 2 * section_height))
fireball2 = pygame.transform.scale(pygame.image.load('assets/images/fireball2.png'),
                                   (1.5 * section_width, 2 * section_height))
hammer = pygame.transform.scale(pygame.image.load('assets/images/hammer.png'),
                                   (2 * section_width, 2 * section_height))
standing = pygame.transform.scale(pygame.image.load('assets/images/mario/standing.png'),
                                  (2 * section_width, 2.5 * section_height))
jumping = pygame.transform.scale(pygame.image.load('assets/images/mario/jumping.png'),
                                 (2 * section_width, 2.5 * section_height))
running = pygame.transform.scale(pygame.image.load('assets/images/mario/running.png'),
                                 (2 * section_width, 2.5 * section_height))
climbing1 = pygame.transform.scale(pygame.image.load('assets/images/mario/climbing1.png'),
                                   (2 * section_width, 2.5 * section_height))
climbing2 = pygame.transform.scale(pygame.image.load('assets/images/mario/climbing2.png'),
                                   (2 * section_width, 2.5 * section_height))
hammer_stand = pygame.transform.scale(pygame.image.load('assets/images/mario/hammer_stand.png'),
                                      (2.5 * section_width, 2.5 * section_height))
hammer_jump = pygame.transform.scale(pygame.image.load('assets/images/mario/hammer_jump.png'),
                                     (2.5 * section_width, 2.5 * section_height))
hammer_overhead = pygame.transform.scale(pygame.image.load('assets/images/mario/hammer_overhead.png'),
                                         (2.5 * section_width, 3.5 * section_height))

start_y = window_height - 2 * section_height
row2_y = start_y - 4 * section_height
row3_y = row2_y - 7 * slope - 3 * section_height
row4_y = row3_y - 4 * section_height
row5_y = row4_y - 7 * slope - 3 * section_height
row6_y = row5_y - 4 * section_height
row6_top = row6_y - 4 * slope
row5_top = row5_y - 8 * slope
row4_top = row4_y - 8 * slope
row3_top = row3_y - 8 * slope
row2_top = row2_y - 8 * slope
row1_top = start_y - 5 * slope
active_level = 0
isClimbing = False
isNearLadder = False

#calling it levels but i aint adding any more than one level

levels = [{'bridges': [(1, start_y, 15), (16, start_y - slope, 3),
                       (19, start_y - 2 * slope, 3), (22, start_y - 3 * slope, 3),
                       (25, start_y - 4 * slope, 3), (28, start_y - 5 * slope, 3),
                       (25, row2_y, 3), (22, row2_y - slope, 3),
                       (19, row2_y - 2 * slope, 3), (16, row2_y - 3 * slope, 3),
                       (13, row2_y - 4 * slope, 3), (10, row2_y - 5 * slope, 3),
                       (7, row2_y - 6 * slope, 3), (4, row2_y - 7 * slope, 3),
                       (2, row2_y - 8 * slope, 2), (4, row3_y, 3),
                       (7, row3_y - slope, 3), (10, row3_y - 2 * slope, 3),
                       (13, row3_y - 3 * slope, 3), (16, row3_y - 4 * slope, 3),
                       (19, row3_y - 5 * slope, 3), (22, row3_y - 6 * slope, 3),
                       (25, row3_y - 7 * slope, 3), (28, row3_y - 8 * slope, 2),
                       (25, row4_y, 3), (22, row4_y - slope, 3),
                       (19, row4_y - 2 * slope, 3), (16, row4_y - 3 * slope, 3),
                       (13, row4_y - 4 * slope, 3), (10, row4_y - 5 * slope, 3),
                       (7, row4_y - 6 * slope, 3), (4, row4_y - 7 * slope, 3),
                       (2, row4_y - 8 * slope, 2), (4, row5_y, 3),
                       (7, row5_y - slope, 3), (10, row5_y - 2 * slope, 3),
                       (13, row5_y - 3 * slope, 3), (16, row5_y - 4 * slope, 3),
                       (19, row5_y - 5 * slope, 3), (22, row5_y - 6 * slope, 3),
                       (25, row5_y - 7 * slope, 3), (28, row5_y - 8 * slope, 2),
                       (25, row6_y, 3), (22, row6_y - slope, 3),
                       (19, row6_y - 2 * slope, 3), (16, row6_y - 3 * slope, 3),
                       (2, row6_y - 4 * slope, 14), (13, row6_y - 4 * section_height, 6),
                       (10, row6_y - 3 * section_height, 3)],
           'ladders': [(12, row2_y + 6 * slope, 2), (12, row2_y + 26 * slope, 2),
                       (25, row2_y + 11 * slope, 4), (6, row3_y + 11 * slope, 3),
                       (14, row3_y + 8 * slope, 4), (10, row4_y + 6 * slope, 1),
                       (10, row4_y + 24 * slope, 2), (16, row4_y + 6 * slope, 5),
                       (25, row4_y + 9 * slope, 4), (6, row5_y + 11 * slope, 3),
                       (11, row5_y + 8 * slope, 4), (23, row5_y + 4 * slope, 1),
                       (23, row5_y + 24 * slope, 2), (25, row6_y + 9 * slope, 4),
                       (13, row6_y + 5 * slope, 2), (13, row6_y + 25 * slope, 2),
                       (18, row6_y - 27 * slope, 4), (12, row6_y - 17 * slope, 2),
                       (10, row6_y - 17 * slope, 2), (12, -5, 13), (10, -5, 13)],
          'hammers': [(4, row6_top + section_height), (4, row4_top+section_height)],
           'target': (13, row6_y - 4 * section_height, 3)}]


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = standing
        self.image = pygame.transform.scale(self.image, (playerWidth, playerHeight))
        self.image2 = running
        self.image2 = pygame.transform.scale(self.image2, (playerWidth, playerHeight))
        self.playerRect = self.image.get_rect()
        self.playerRect.left = 150
        self.playerRect.top = screen_height - 200
        self.isImageFacingLeft = False
        self.framesSinceSwitch = 0
        self.verticalSpeed = 0
        self.horizontalSpeed = 200
        self.acceleration = 15
        self.jumpSpeed = -7000
        self.isJumping = False
        self.isLineClipping = False
        self.isClimbing = False
        self.isMoving = False

    def draw(self):
        if self.isMoving:
            if self.framesSinceSwitch < 4:
                self.screen.blit(self.image2, self.playerRect)
            else:
                self.screen.blit(self.image, self.playerRect)

            self.framesSinceSwitch = (self.framesSinceSwitch + 1) % 8
        else:
            self.screen.blit(self.image, self.playerRect)
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
            self.playerRect.move_ip(0, self.verticalSpeed * dt) #the player was jittering so just make it jitter faster than the frame rate

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
            self.image = pygame.transform.flip(self.image, True, False) 
            self.image2 = pygame.transform.flip(self.image2, True, False)
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
            self.image = pygame.transform.flip(self.image, True, False) 
            self.image2 = pygame.transform.flip(self.image2, True, False)
            self.isImageFacingLeft = False
                    
        if self.playerRect.right + self.horizontalSpeed * dt < window_width - 2:
            self.playerRect.move_ip(self.horizontalSpeed * dt, 0)
        
class Bridge:
    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.top = self.draw()

    def draw(self):
        line_width = 3
        platform_color = (225, 51, 100)
        for i in range(self.length):
            bot_coord = self.y_pos + section_height
            left_coord = self.x_pos + (section_width * i)
            mid_coord = left_coord + (section_width * 0.5)
            right_coord = left_coord + section_width
            top_coord = self.y_pos
            pygame.draw.line(screen, platform_color, (left_coord, top_coord),
                             (right_coord, top_coord), line_width)
            pygame.draw.line(screen, platform_color, (left_coord, bot_coord),
                             (right_coord, bot_coord), line_width)
            pygame.draw.line(screen, platform_color, (left_coord, bot_coord),
                             (mid_coord, top_coord), line_width)
            pygame.draw.line(screen, platform_color, (mid_coord, top_coord),
                             (right_coord, bot_coord), line_width)
        top_line = pygame.Rect(self.x_pos, self.y_pos, self.length * section_width, 2)
        return top_line

class Ladder:
    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.body = self.draw()

    def draw(self):
        line_width = 3
        lad_color = 'light blue'
        lad_height = 0.6
        for i in range(self.length):
            top_coord = self.y_pos + lad_height * section_height * i
            bot_coord = top_coord + lad_height * section_height
            mid_coord = (lad_height / 2) * section_height + top_coord
            left_coord = self.x_pos
            right_coord = left_coord + section_width
            pygame.draw.line(screen, lad_color, (left_coord, top_coord), (left_coord, bot_coord), line_width)
            pygame.draw.line(screen, lad_color, (right_coord, top_coord), (right_coord, bot_coord), line_width)
            pygame.draw.line(screen, lad_color, (left_coord, mid_coord), (right_coord, mid_coord), line_width)
        body = pygame.Rect(self.x_pos, self.y_pos - section_height,
                           section_width, lad_height * self.length * section_height + section_height)
        return body

def drawMap():
    platforms = []
    climbers = []
    ladder_objs = []
    bridge_objs = []

    ladders = levels[active_level]['ladders']
    bridges = levels[active_level]['bridges']

    for ladder in ladders:
        ladder_objs.append(Ladder(*ladder))
        if ladder[2] >= 3:
            climbers.append(ladder_objs[-1].body)
    for bridge in bridges:
        bridge_objs.append(Bridge(*bridge))
        platforms.append(bridge_objs[-1].top)

    return platforms, climbers

def main():
  
    clock = pygame.time.Clock()
    running = True
    dt = 0

    player = Player(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.isMoving = False

        screen.fill((0, 0, 0))

        platforms, ladders = drawMap()

        player.gravity(platforms, dt)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.jump(dt)
        if keys[pygame.K_UP]:
            player.climb(ladders, True, dt)
        if keys[pygame.K_DOWN]:
            player.climb(ladders, False, dt)
        if keys[pygame.K_LEFT]:
            player.moveLeft(ladders, dt)
        if keys[pygame.K_RIGHT]:
            player.moveRight(ladders, dt)

        player.draw()

        pygame.display.flip()
        dt = clock.tick(30) / 1000

    pygame.quit()

if __name__ == "__main__":
    main()
