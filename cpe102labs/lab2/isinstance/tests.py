import unittest
import math

from classes import *
from area import area

class Tests(unittest.TestCase):
   def test1(self):
      self.assertAlmostEqual(area(Circle(2)), 4 * math.pi) 

   def test2(self):
      self.assertAlmostEqual(area(Square(9)), 81) 

   def test3(self):
      self.assertAlmostEqual(area(Rectangle(2, 7)), 14) 

   def test4(self):
      self.assertRaises(TypeError, area, 3) 


if __name__ == '__main__':
   unittest.main()
