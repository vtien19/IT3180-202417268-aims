import contextlib
import io
import unittest

from aims.cart import Cart, MAX_NUMBERS_ORDERED
from aims.dvd import DigitalVideoDisc


class TestCart(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()

    def add(self, title):
        with contextlib.redirect_stdout(io.StringIO()):
            return self.cart.add_dvd(DigitalVideoDisc(title, cost=1.0))

    def test_add_dvd_below_limit(self):
        results = [self.add(f"DVD {i}") for i in range(MAX_NUMBERS_ORDERED)]
        self.assertTrue(all(results))
        self.assertEqual(len(self.cart.items), MAX_NUMBERS_ORDERED)

    def test_add_dvd_until_full(self):
        for i in range(MAX_NUMBERS_ORDERED):
            self.add(f"DVD {i}")
        self.assertFalse(self.add("DVD 21"))
        self.assertEqual(len(self.cart.items), MAX_NUMBERS_ORDERED)


if __name__ == "__main__":
    unittest.main()
