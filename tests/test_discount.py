import contextlib
import io
import unittest

from aims.cart import Cart
from aims.dvd import DigitalVideoDisc


class TestDiscount(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()
        with contextlib.redirect_stdout(io.StringIO()):
            self.cart.add_dvd(DigitalVideoDisc("A", cost=60.0))
            self.cart.add_dvd(DigitalVideoDisc("B", cost=40.0))

    def test_discount_20_percent(self):
        self.assertAlmostEqual(self.cart.total_cost_with_discount(20), 80.0)

    def test_invalid_percent_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.cart.total_cost_with_discount(150)


if __name__ == "__main__":
    unittest.main()
