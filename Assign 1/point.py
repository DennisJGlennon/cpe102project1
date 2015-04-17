class Point:
   def __init__(self, x, y):
      self.x = x
      self.y = y

   def adjacent(self, pt2):
      return ((self.x == pt2.x and abs(self.y - pt2.y) == 1) or
         (self.y == pt2.y and abs(self.x - pt2.x) == 1))
