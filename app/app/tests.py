"""
sample tests
"""

from django.test import SimpleTestCase

from app import calc

class CalcTests(SimpleTestCase):
    """Test the calc module"""
    
    def test_add_numners(self):
        """Test adding numbers togethers"""
        res = calc.add(5, 6)
        
        self.assertEqual(res, 11)
