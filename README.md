<p align="center"><img width=80% src="https://raw.githubusercontent.com/theaustinator/peep-dis/master/static/peep_dis_banner.jpg"></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![GitHub Issues](https://img.shields.io/github/issues/TheAustinator/peep-dis.svg)](https://github.com/TheAustinator/peep-dis/issues)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
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
**Install**
```
pip install peepdis
```
**Import**
```python
from peepdis import peep
```
**Peep Imported Objects**
```python
import pandas as pd

df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
peep(df)
```
**Peep Your Own Objects**
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
**Include Builtins (i.e. Magics)**

Controls the inclusion of "magic" methods and attributes, which are denoted by leading and trailing double underscores -- e.g., "__init__". They are excluded by default.
```python
peep(sq, builtins=True)
```
**Include Private Attributes and Methods**

Controls the inclusion of private methods and attributes, which are denoted by a single leading underscore -- e.g., "_method_name". They are excluded by default.
```python
peep(sq, privates=True)
```
**Print Docstrings With Output**
```python
peep(sq, docstrings=True)
```
**Truncate Output Length**

Controls maximum number of characters for each method or attribute output. No truncation will occur if `None` or `0`. Set at 250 characters by default.
```python
peep(sq, truncate_len=None)
```
**In the Debugger**

To call `peep` in the debugger, it must be wrapped in a print statement. This is consistent across pdb, ipdb, PyCharm's built-in debugger, etc.
```python
(Pdb) print(peep(sq))
```

## Example Usage
**I. The Mystery Object**

We have a simple `mystery_obj` which contains an array of San Francisco temperatures somewhere within it, but we don't know where. We could call `dir`, then iteratively check each method/attribute, or we could just `peep` the object.

![Example 1](/static/peep_mystery_obj.png)

We can quickly identify `stdtemp` as the attribute we need.
Built-ins are filtered out, and outputs for the rest of the attributes and methods without positional arguments are printed. Methods are colored purple, and attributes are cyan. The outputs from methods requiring positional arguments are grayed out to allow us to skim others more quickly.

**II. What's the name of that method?**

We have a `DataFrame` with the columns `temp` and `humidity` for San Francisco, which we want to convert to a narrow data model for an API we are building. There's a one-liner for this, but nothing stands out in `dir`, and nothing turns up on Stack Overflow. If we peep the DataFrame, we'll quickly identify `melt` as the method we need.

![Example 2 call](/static/peep_df.png)
![Example 2 output](/static/peep_df_output.png)

## Upcoming Features
**Argument Forging**

Sometimes a method requires one simple argument to run, like an index. By forging simple arguments like these, we can see example outputs from methods that we wouldn't otherwise be able to see. The sample code which this feature will be based on can be found in the accompanying blog post at ____.

**Tracking State Changes**

Often, a method call changes the state of the object. Tracking state changes would allow us to see understand what these types of methods do. The sample code which this feature will be based on can be found in the accompanying blog post at ____.

**Customizable Preferences and Color Scheme**
