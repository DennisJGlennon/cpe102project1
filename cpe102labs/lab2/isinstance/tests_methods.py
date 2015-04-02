import unittest
import math

from classes_methods import *
from area import area

class Tests(unittest.TestCase):
   def test1(self):
      self.assertAlmostEqual(Circle(2).area(), 4 * math.pi) 

   def test2(self):
      self.assertAlmostEqual(Square(9).area(), 81) 

   def test3(self):
      self.assertAlmostEqual(Rectangle(2, 7).area(), 14) 


if __name__ == '__main__':
   unittest.main()
