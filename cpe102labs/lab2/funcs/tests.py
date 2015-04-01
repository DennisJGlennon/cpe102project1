import funcs
import unittest

class Tests(unittest.TestCase):
   def test1(self):
      self.assertEqual(funcs.map(lambda x: x**2, [1,2,3]), [1,4,9])

   def test2(self):
      self.assertEqual(funcs.map(lambda x: x+9, [1,2,3]), [10, 11, 12])

   def test3(self):
      f = funcs.add(10)
      self.assertEqual(f(2), 12)
      self.assertEqual(f(9), 19)
      
   def test4(self):
      f = funcs.add(-2)
      self.assertEqual(f(2), 0)
      self.assertEqual(f(9), 7)

   def test5(self):
      counter = funcs.create_counter(2)
      self.assertEqual(counter(), 2)
      self.assertEqual(counter(), 3)
      
   def test6(self):
      counter1 = funcs.create_counter(2)
      counter2 = funcs.create_counter(10)
      self.assertEqual(counter1(), 2)
      self.assertEqual(counter2(), 10)
      self.assertEqual(counter1(), 3)
      self.assertEqual(counter2(), 11)


if __name__ == '__main__':
   unittest.main()
