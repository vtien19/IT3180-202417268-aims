import unittest

from aims.dvd import DigitalVideoDisc
from aims.search import search_by_category, search_by_title


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.items = [
            DigitalVideoDisc("The Lion King"),
            DigitalVideoDisc("Star Wars"),
            DigitalVideoDisc("Aladdin"),
        ]

    def test_search_by_category(self):
        items = [
            DigitalVideoDisc("The Lion King", "Animation"),
            DigitalVideoDisc("Star Wars", "Science Fiction"),
            DigitalVideoDisc("Aladdin", "Animation"),
        ]
        result = search_by_category(items, "Animation")
        self.assertEqual([dvd.title for dvd in result], ["The Lion King", "Aladdin"])

    def test_search_by_title_found(self):
        result = search_by_title(self.items, "Lion")
        self.assertEqual([dvd.title for dvd in result], ["The Lion King"])

    def test_search_by_title_ignores_case(self):
        result = search_by_title(self.items, "lion")
        self.assertEqual([dvd.title for dvd in result], ["The Lion King"])


if __name__ == "__main__":
    unittest.main()
