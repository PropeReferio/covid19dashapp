import unittest
from newapp import trend_colors
import pandas as pd 
from pandas import DataFrame as df 

testframe = df([-15, -140, -10000, -50, -90, 10000, 2000, 90, 60,
                30, 5, 0])
testframe['Percent Change'] = df([-15, -140, -10000, -50, -90, 10000, 2000, 90,
                                    60, 30, 5, 0])

class TestTrendColors(unittest.TestCase):
    def test_range(self):
        self.assertEqual(trend_colors(testframe), [1, 9, 9, 5, 9, 19, 19, 19, 
        16, 13, 10, 20])