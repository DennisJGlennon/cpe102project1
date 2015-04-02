import math
import random
import sys, pygame
from pygame.locals import *

from ball import *
import colors

WIDTH = 600
HEIGHT = 600


def initialize_scene():
   balls = []
   balls.append(Ball(300, 40, 40, colors.RED, RIGHT, DOWN))
   balls.append(Ball(280, 300, 20, colors.GREEN, LEFT, UP))
   balls.append(Ball(300, 100, 20, colors.PURPLE, NEUTRAL, DOWN))

   return balls


# draw the scene 
def draw(screen, balls) : 
   screen.fill(colors.GREY)        
   for ball in balls:
      ball.draw_ball(screen)

def move(balls, width, height):
   for ball in balls:
      ball.move_ball(width, height, balls)

def event_loop(screen, balls, width, height):
   while True:
      for event in pygame.event.get():
         if event.type == QUIT: return
         elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
               print("right key")
            if event.key == pygame.K_LEFT:
               print("left key")

      draw(screen, balls)
      pygame.display.flip()

      move(balls, width, height)

#function to start up the main drawing
def main():
   pygame.init()
   width = WIDTH
   height = HEIGHT
   screen = pygame.display.set_mode((width, height))

   balls = initialize_scene()

   event_loop(screen, balls, width, height)

if __name__ == '__main__':
   main()

