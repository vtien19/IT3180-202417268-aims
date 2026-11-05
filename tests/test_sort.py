import contextlib
import io
import unittest

from aims.cart import Cart
from aims.dvd import DigitalVideoDisc


class TestSort(unittest.TestCase):
    def test_sort_by_title_and_by_cost(self):
        cart = Cart()
        with contextlib.redirect_stdout(io.StringIO()):
            for title, cost in [("Star Wars", 24.95), ("Aladdin", 18.99),
                                ("The Lion King", 19.95), ("Aladdin", 20.50)]:
                cart.add_dvd(DigitalVideoDisc(title, cost=cost))

        cart.sort_by_title()
        self.assertEqual([(dvd.title, dvd.cost) for dvd in cart.items],
                         [("Aladdin", 20.50), ("Aladdin", 18.99),
                          ("Star Wars", 24.95), ("The Lion King", 19.95)])

        cart.sort_by_cost()
        self.assertEqual([dvd.cost for dvd in cart.items], [24.95, 20.50, 19.95, 18.99])


if __name__ == "__main__":
    unittest.main()
