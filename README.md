# Data Detector

[![CircleCI](https://circleci.com/gh/iatlab/data_detector.svg?style=svg)](https://circleci.com/gh/iatlab/data_detector)

Detecting data in spreadsheet files. The detector was trained with thousands of annotated spreadsheets. 
The trained model is very accurate: 99.3% in a dataset including 2,505 spreadsheets.

## Data?
Here, data are defined as numbers that are measured for making some insights.
For example, running speed of animals, population in a country, and the number of customers per week.
On the other hand, IDs of products, telephone numbers, and zipcodes, which are arbitrarily selected, are not data.

## Installation
`data_detector` can be installed by

```bash
$ pip install git+https://github.com/iatlab/data_detector.git
```

## Usage
```python
>>> from data_detector import DataDetector
>>> dd = DataDetector()
>>> dd.detect("/path/to/statistics.xlsx") # filepath to a spreadsheet with two data sheets
[0.98, 0.99]
>>> dd.detect("/path/to/application_form.xlsx") # filepath to a spreadsheet with a non-data sheet
[0.02]
```

`DataDetector.detect` returns a list of values,
which indicate the probability of being data for each sheet in the spreadsheet.
