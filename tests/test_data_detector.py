import os
from unittest import TestCase
from nose.tools import eq_, ok_, raises
from pprint import pprint
#
from data_detector import DataDetector

class DataDetectorTestCase(TestCase):
    PWD = os.path.dirname(os.path.abspath(__file__))

    def test_init(self):
        dd = DataDetector()
        eq_(dd.model.__class__.__name__,      "GradientBoostingClassifier")
        eq_(dd.vectorizer.__class__.__name__, "DictVectorizer")
        eq_(dd.scaler.__class__.__name__,     "StandardScaler")

    def test_detect(self):
        dd = DataDetector()
        test_file1 = os.path.join(self.PWD, "test1.xlsx")
        res = dd.detect(test_file1)
        ok_(res[0] > 0.5)
        test_file2 = os.path.join(self.PWD, "test2.xlsx")
        res = dd.detect(test_file2)
        ok_(res[0] < 0.5)
