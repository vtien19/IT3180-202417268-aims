import unittest

from aims.dvd import DigitalVideoDisc
from aims.search import search_by_title


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.items = [
            DigitalVideoDisc("The Lion King"),
            DigitalVideoDisc("Star Wars"),
            DigitalVideoDisc("Aladdin"),
        ]

    def test_search_by_title_found(self):
        result = search_by_title(self.items, "Lion")
        self.assertEqual([dvd.title for dvd in result], ["The Lion King"])


if __name__ == "__main__":
    unittest.main()
