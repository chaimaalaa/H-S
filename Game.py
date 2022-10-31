import os
import sys
import random
import pygame
import numpy as np


# Class for the Hider (yellow square) and seeker (red square) 
class Player(object):
    
    def __init__(self,x,y,type):
        self.rect = pygame.Rect(x,y, 30, 30)
        self.type = type

    def move(self, dx, dy):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

# Nice class to hold a wall rect
class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 30, 30)

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Get to the red square!")
screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()
walls = [] # List to hold the walls
player1 = Player(180,90,"H") # Create the Hider
end = Player(240,240,"S") # Create the Seeker


# Holds the level layout in a list of strings.
level = [
    "WWWWWWWWWWWWWW",
    "W            W",
    "W  W     W   W",
    "W  WWW   WWW W",
    "W  WWW   WWW W",
    "W  WWW   WW  W",
    "W            W",
    "W   W        W",
    "W  WWW   WWW W",
    "W  WWW   WW  W",
    "W  WWW   WW  W",
    "W    W   WW  W",
    "W            W",
    "WWWWWWWWWWWWWW",
]


# Parse the level string above. W = wall
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        x += 30
    y += 30
    x = 0

# Running the game  
running = True
while running:
    clock.tick(60)

    # Condition to make the red square seek for the yellow square
    if(end.rect.x < player1.rect.x and end.rect.y <= player1.rect.y):
        end.move(1,1)
    elif(end.rect.x > player1.rect.x and end.rect.y <= player1.rect.y):
        end.move(-1,1)
    elif(end.rect.x <= player1.rect.x and end.rect.y > player1.rect.y):
        end.move(1,-1)
    elif(end.rect.x >= player1.rect.x and end.rect.y > player1.rect.y):
        end.move(-1,-1)

    # Moving the yellow square with keys  
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player1.move(-3, 0)
    if key[pygame.K_RIGHT]:
        player1.move(3, 0)
    if key[pygame.K_UP]:
        player1.move(0, -3)
    if key[pygame.K_DOWN]:
        player1.move(0, 3)

    # Keys for ending the game
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    # Ending the game the red suqare catches the yellow square
    if player1.rect.colliderect(end):
        pygame.quit()
        sys.exit()

    # Draw the scene
    screen.fill((255, 255, 255))
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 0), wall.rect)
    pygame.draw.rect(screen, (255, 200, 0), player1.rect)
    pygame.draw.rect(screen, (255, 0, 0), end.rect)
    pygame.display.flip()
    clock.tick(360)

pygame.quit()