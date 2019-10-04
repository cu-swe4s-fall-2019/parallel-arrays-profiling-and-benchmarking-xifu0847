import plot_gtex
import unittest


class TestPlotGtex(unittest.TestCase):

    def setUp(self):
        self.linear_data = [1, 3, 5, 6, 7]
        self.binary_data = [[1, 2], [2, 3], [3, 5]]

    def test_linear_search_with_val(self):
        res = plot_gtex.linear_search(3, self.linear_data)
        self.assertEqual(res, 1)

    def test_linear_search_without_val(self):
        res = plot_gtex.linear_search(0, self.linear_data)
        self.assertEqual(res, -1)

    def test_linear_search_empty_list(self):
        res = plot_gtex.linear_search(0, [])
        self.assertEqual(res, -1)

    def test_binary_search_with_val(self):
        res = plot_gtex.binary_search(3, self.binary_data)
        self.assertEqual(res, 5)

    def test_binary_search_without_val(self):
        res = plot_gtex.binary_search(0, self.binary_data)
        self.assertEqual(res, -1)

    def test_binary_search_empty_list(self):
        res = plot_gtex.binary_search(0, [])
        self.assertEqual(res, -1)
