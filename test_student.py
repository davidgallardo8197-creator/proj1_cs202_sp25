import unittest
from proj1 import *


class TestStudent(unittest.TestCase):

    def setUp(self):
        self.rect1 = GlobeRect(0.0, 10.0, 0.0, 10.0)
        self.rect2 = GlobeRect(0.0, 5.0, 0.0, 5.0)

        self.region1 = Region(self.rect1, "A", "other")
        self.region2 = Region(self.rect2, "B", "forest")

        self.rc1 = RegionCondition(self.region1, 2025, 1000, 5000.0)
        self.rc2 = RegionCondition(self.region2, 2025, 2000, 4000.0)
        self.rc_zero = RegionCondition(self.region1, 2025, 0, 5000.0)

    def test_emissions_per_capita(self):
        self.assertAlmostEqual(emissions_per_capita(self.rc1), 5.0)

    def test_emissions_per_capita_zero_pop(self):
        self.assertEqual(emissions_per_capita(self.rc_zero), 0.0)

    def test_area(self):
        self.assertTrue(area(self.rect1) > 0)

    def test_emissions_per_square_km(self):
        self.assertTrue(emissions_per_square_km(self.rc1) > 0)

    def test_densest(self):
        self.assertEqual(densest([self.rc1, self.rc2]), "B")

    def test_project_condition(self):
        projected = project_condition(self.rc1, 5)
        self.assertEqual(projected.year, 2030)
        self.assertEqual(projected.region, self.rc1.region)
        self.assertTrue(projected.pop >= self.rc1.pop)


if __name__ == "__main__":
    unittest.main()