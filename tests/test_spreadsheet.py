import os
from unittest import TestCase
from nose.tools import eq_, ok_, raises
from pprint import pprint
#
from data_detector.spreadsheet import Spreadsheet

class SpreadsheetTestCase(TestCase):
    PWD = os.path.dirname(os.path.abspath(__file__))

    def test_parse(self):
        test_file1 = os.path.join(self.PWD, "test1.xlsx")
        ss = Spreadsheet.parse(test_file1)
        eq_(len(ss), 1)
        eq_(len(ss[0]), 38)
        eq_(ss[0][2][0], "市区町村")

    def test_parse_from_stream(self):
        test_file1 = os.path.join(self.PWD, "test1.xlsx")
        with open(test_file1, "rb") as f:
            ss = Spreadsheet.parse_xl(f)
        eq_(len(ss), 1)
        eq_(len(ss[0]), 38)
        eq_(ss[0][2][0], "市区町村")

    def test_parse_from_csv(self):
        test_file3 = os.path.join(self.PWD, "test3.csv")
        ss = Spreadsheet.parse_csv(test_file3)
        eq_(len(ss), 1)
        eq_(len(ss[0]), 5)
        eq_(ss[0][2][0], "5")

    def test_truncate_rows(self):
        test_file1 = os.path.join(self.PWD, "test1.xlsx")
        ss = Spreadsheet.parse(test_file1, truncate_rows=3)
        eq_(len(ss), 1)
        eq_(len(ss[0]), 3)
        ss = Spreadsheet.parse_xl(test_file1, truncate_rows=3)
        eq_(len(ss), 1)
        eq_(len(ss[0]), 3)

        test_file3 = os.path.join(self.PWD, "test3.csv")
        ss = Spreadsheet.parse_csv(test_file3, truncate_rows=3)
        eq_(len(ss[0]), 3)
