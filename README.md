<p align="center"><img width=80% src="https://raw.githubusercontent.com/theaustinator/peep-dis/master/static/peep_dis_banner.jpg"></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![Build Status](https://travis-ci.org/_insert_url_)](https://travis-ci.org/_insert_url_)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub Issues](https://img.shields.io/github/issues/TheAustinator/peep-dis.svg)](https://github.com/TheAustinator/peep-dis/issues)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## A colorful CLI object inspector for python

**peep dis (verb phrase, imperative)**: "Check this out" or "Hey! Have a look at this."



<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#features">Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#related">Related</a> •
  <a href="#license">License</a>
</p>


## Overview

<p align="center"><img width=80% src="https://raw.githubusercontent.com/theaustinator/peep-dis/master/static/peep_dis_demo.gif"></p>

### Features
* Evaluate attributes and callables
* Calls run on duplicate objects to avoid state alteration
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
Use on external objects
```python
import pandas as pd

df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
peep(df)
```
Use on your own objects
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
Include builtins
```python
peep(sq, builtins=True)
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
