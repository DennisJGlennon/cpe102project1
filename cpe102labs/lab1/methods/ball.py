import pygame

UP = -1
DOWN = 1
LEFT = -1
RIGHT = 1
NEUTRAL = 0

class Ball:
   def __init__(self, x, y, radius, color, dx, dy):
      self.x = x
      self.y = y
      self.radius = radius
      self.color = color
      self.dx = dx
      self.dy = dy

   def draw_ball(self, screen):
      pygame.draw.ellipse(screen, self.color, 
         pygame.Rect(self.x - self.radius, self.y - self.radius, 
            self.radius * 2, self.radius * 2)) 

