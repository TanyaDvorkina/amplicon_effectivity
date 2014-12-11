__author__ = 'Anton Bragin'

from unittest import TestCase

import oligo_calculator

class TestOligoCalculator(TestCase):

    def setUp(self):
        self.calculator = oligo_calculator.OligoCalculator()

    def test_calculation(self):
        self.assertAlmostEquals(26.66, self.calculator.caclulate('aaaaaaaaaaaaaaaa')[0])
        self.assertAlmostEquals(-6.00, self.calculator.caclulate('aaaaaaaaaaaaaaaa')[1])
        self.assertAlmostEquals(60.45, self.calculator.caclulate('ATTGCTGATGCGGGATTAGCTGATGTAG')[0])
        self.assertAlmostEquals(-25.34, self.calculator.caclulate('ATTGCTGATGCGGGATTAGCTGATGTAG')[1])

