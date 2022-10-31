import gym
from gym import spaces
from stable_baselines3 import DQN
from stable_baselines3.common.evaluation import evaluate_policy
import numpy as np
import pygame
import os
import sys


class Player(object):
  
  def __init__(self,x,y,type,walls):
      self.x = x
      self.y = y
      self.rect = pygame.Rect(self.x,self.y, 30, 30)
      self.type = type
      self.walls = walls

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
      for wall in self.walls:
          if self.rect.colliderect(wall.rect):
              if dx > 0: # Moving right; Hit the left side of the wall
                  self.rect.right = wall.rect.left
              if dx < 0: # Moving left; Hit the right side of the wall
                  self.rect.left = wall.rect.right
              if dy > 0: # Moving down; Hit the top side of the wall
                  self.rect.bottom = wall.rect.top
              if dy < 0: # Moving up; Hit the bottom side of the wall
                  self.rect.top = wall.rect.bottom


class Wall(object):  
  def __init__(self, pos):
      self.rect = pygame.Rect(pos[0], pos[1], 30, 30)
        

class HideNSeekEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {"render.modes": ["human"]}
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
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    def __init__(self):
      super(HideNSeekEnv, self).__init__()
      # Define action and observation space
      # They must be gym.spaces objects
      # Example when using discrete actions:
      # Initialise pygame
      os.environ["SDL_VIDEO_CENTERED"] = "1"
      pygame.init()

      # Set up the display
      pygame.display.set_caption("Escape from red square!")
      self.screen = pygame.display.set_mode((500, 500))

      self.clock = pygame.time.Clock()
      self.walls = [] # List to hold the walls
      self.game_over = False
      x = y = 0
      for row in self.level:
          for col in row:
              if col == "W":
                  self.walls.append(Wall((x,y)))
              x += 30
          y += 30
          x = 0
      self.player1 = Player(30,30,"H",self.walls) # Create the player  
      self.end = Player(240,240,"S",self.walls)
      self.prev_player_x = self.player1.x  
      self.prev_player_y = self.player1.y  
      nombre_actions = 4
      nombre_observations = 4
      self.action_space = spaces.Discrete(nombre_actions)
      # Example for using image as input (channel-first; channel-last also works):
      self.observation_space = spaces.Box(low=-np.inf, high=np.inf,shape=(nombre_observations,), dtype=np.uint8)

    def step(self, action):
      self.clock.tick(360) 
      if(self.end.rect.x < self.player1.rect.x and self.end.rect.y < self.player1.rect.y):
        self.end.move(1,0)
        self.end.move(0,1)
        # self.end.rect = pygame.Rect(self.end.x,self.end.y,30, 30)
      elif(self.end.rect.x > self.player1.rect.x and self.end.rect.y < self.player1.rect.y):
        self.end.move(-1,0)
        self.end.move(0,1)
        # self.end.rect = pygame.Rect(self.end.rect.x,self.end.rect.y,30, 30)
      elif(self.end.rect.x < self.player1.rect.x and self.end.rect.y > self.player1.rect.y):
        self.end.move(1,0)
        self.end.move(0,-1)
        # self.end.rect = pygame.Rect(self.end.rect.x,self.end.rect.y,30, 30)
      elif(self.end.rect.x > self.player1.rect.x and self.end.rect.y > self.player1.rect.y):
        self.end.move(-1,0)
        self.end.move(0,-1)
        # self.end.rect = pygame.Rect(self.end.x,self.end.rect.y,30, 30)
      elif(self.end.rect.x == self.player1.rect.x and self.end.rect.y > self.player1.rect.y):
        self.end.move(0,-1)
        # self.end.rect = pygame.Rect(self.end.x,self.end.rect.y,30, 30)
      elif(self.end.rect.x == self.player1.rect.x and self.end.rect.y < self.player1.rect.y):
        self.end.move(0,1)
        # self.end.rect = pygame.Rect(self.end.x,self.end.rect.y,30, 30)
      elif(self.end.rect.x > self.player1.rect.x and self.end.rect.y == self.player1.rect.y):
        self.end.move(-1,0)
        # self.end.rect = pygame.Rect(self.end.x,self.end.rect.y,30, 30)
      elif(self.end.rect.x < self.player1.rect.x and self.end.rect.y == self.player1.rect.y):
        self.end.move(1,0)
        # self.end.rect = pygame.Rect(self.end.x,self.end.rect.y,30, 30)

      if action == self.LEFT:
          self.player1.move(-3, 0)
      if action == self.RIGHT:
          self.player1.move(3, 0)
      if action == self.UP:
          self.player1.move(0, -3)
      if action == self.DOWN:
          self.player1.move(0, 3)

      reward = 0
      if self.player1.rect.colliderect(self.end.rect):
          reward = -100
      elif abs(self.player1.rect.x - self.end.rect.x) + abs(self.player1.rect.y - self.end.rect.y) > abs(self.prev_player_x - self.end.rect.x) + abs(self.prev_player_y - self.end.rect.y):
          reward = 100
      elif abs(self.player1.rect.x - self.end.rect.x) + abs(self.player1.rect.y - self.end.rect.y) > abs(self.prev_player_x - self.end.rect.x) + abs(self.prev_player_y - self.end.rect.y):
          reward = -1

      print(reward)  
      self.prev_player_x = self.player1.rect.x
      self.prev_player_y = self.player1.rect.y
      done = self.game_over
      info = {}    
      return np.array([self.player1.rect.x, self.player1.rect.y, self.end.rect.x, self.end.rect.y], dtype=np.float32), reward, done, info
    def reset(self):
      self.walls = [] # List to hold the walls
      self.game_over = False
      x = y = 0
      for row in self.level:
          for col in row:
              if col == "W":
                self.walls.append(Wall((x,y)))
              # if col == "E":
              #     self.end = pygame.Rect(x,y,30, 30)
              x += 30
          y += 30
          x = 0
      self.player1 = Player(30,30,"H",self.walls) # Create the player  
      self.end = Player(240,240,"S",self.walls) # Create the player 
      self.prev_player_x = self.player1.x  
      self.prev_player_y = self.player1.y 
      return np.array([self.player1.rect.x, self.player1.rect.y, self.end.rect.x, self.end.rect.y], dtype=np.float32)  # reward, done, info can't be included
    
    def render(self, mode="human"):
      self.screen.fill((255, 255, 255))
      for wall in self.walls:
        pygame.draw.rect(self.screen, (0, 0, 0), wall.rect)
      pygame.draw.rect(self.screen, (255, 200, 0), self.player1.rect)
      pygame.draw.rect(self.screen, (255, 0, 0), self.end.rect)
      pygame.display.update()

    def close (self):
      pygame.quit()
      sys.exit()



env = HideNSeekEnv()


# model = DQN("MlpPolicy", env, verbose=1)
# model.learn(total_timesteps=1000)
# model.save("HideNSeek")

# # del model # remove to demonstrate saving and loading

model = DQN.load("HideNSeek")
# mean_reward, std_reward = evaluate_policy(model,env, n_eval_episodes=1)

obs = env.reset()
while True:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
      obs = env.reset()