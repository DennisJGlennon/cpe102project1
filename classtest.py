class Outer:
   def __init__(self, point, other):
      self.point = point
      self.other = other

   def move_horiz(self.point, dist):
      self.point.x += dist

class Inner:
   def __init__(self, x, y):
      self.x = x
      self.y = y
   def move_horiz(self, dist):
      self.x += dist

if __name__ == '__main__':
   inner = Inner(1, 2)
   outer = Outer(inner, 3)
   outer.move_horiz(5)
   print outer.point.x, outer.point.y 
