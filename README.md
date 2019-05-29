<p align="center"><img width=80% src="https://raw.githubusercontent.com/theaustinator/peep-dis/master/static/peep_dis_banner.jpg"></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![GitHub Issues](https://img.shields.io/github/issues/TheAustinator/peep-dis.svg)](https://github.com/TheAustinator/peep-dis/issues)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[![PyPI version](https://badge.fury.io/py/peepdis.svg)](https://badge.fury.io/py/peepdis)
[![Build Status](https://travis-ci.org/TheAustinator/peep-dis.svg?branch=master)](https://travis-ci.org/TheAustinator/peep-dis)


## A colorful CLI object inspector for python

**peep dis (verb phrase, imperative)**: "Check this out" or "Hey! Have a look at this."



<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#features">Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#upcoming-features">Upcoming Features</a>
</p>


## Overview

<p align="center"><img width=80% src="https://raw.githubusercontent.com/theaustinator/peep-dis/master/static/peep_dis_demo.gif"></p>

### Features
* Evaluate and color codes attributes and callables
* Duplicates object to avoid state alterations
* Choose whether builtin and private attributes and methods are included
* Attempt to forge arguments from type hints (in development)
* Allow user specified arguments (in development)

## Usage
```
pip install peepdis
```
Import
```python
from peepdis import peep
```
Peep external objects
```python
import pandas as pd

df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
peep(df)
```
Peep your own objects
```python
class Square:
    def __init__(self, a, b, name=None):
        self.a = a
        self.b = b
        self.name = name
    
    def ratio(self):
        return self.a / self.b
    
    def area(self):
        return self.a * self.b
 
 
sq = Rect(4, 4)
peep(sq)
```
Include builtins (i.e. dunders)
```python
peep(sq, builtins=True)
```
Include private attributes and methods
```python
peep(sq, privates=True)
```
Print docstrings with output
```python
peep(sq, docstrings=True)
```
Include long outputs (truncates at 250 char by default)
```python
peep(sq, truncate_len=None)
```
Use in debugger
```python
(Pdb) print(peep(sq))
```

## Upcoming Features
* Include/exclude private methods and attributes
* Detect and display resultant state changes
* User specified arguments
* Argument forging from type hints, docstrings, or by brute force
* Optionally include docstrings
* Modify color scheme and other preferences
