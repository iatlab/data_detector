# -*- coding:utf-8 -*-
from setuptools import setup

setup(
    name = "data_detector",
    packages = ["data_detector"],
    version = "0.0.1",
    description = "Detecting data in spreadsheet files. "\
                  "The detector was trained with thousands of annotated spreadsheets.",
    author = "Makoto P. Kato",
    author_email = "mpkato@acm.org",
    license     = "MIT License",
    url = "https://github.com/iatlab/data_detector",
    setup_requires = [
        'numpy' # this required by scikit-learn
    ],
    install_requires = [
        'scikit-learn',
        'xlrd',
        'mojimoji',
    ],
    package_data = {
        'data_detector': ['*.pkl'],
    }
)

