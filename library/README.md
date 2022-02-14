# MCP9600 Thermocouple Temperature Sensor

[![Build Status](https://shields.io/github/workflow/status/pimoroni/mcp9600-python/Python%20Tests.svg)](https://github.com/pimoroni/mcp9600-python/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/mcp9600-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/mcp9600-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/mcp9600.svg)](https://pypi.python.org/pypi/mcp9600)
[![Python Versions](https://img.shields.io/pypi/pyversions/mcp9600.svg)](https://pypi.python.org/pypi/mcp9600)


# Installing

Stable library from PyPi:

* Just run `python3 -m pip install mcp9600`

Latest/development library from GitHub:

* `git clone https://github.com/pimoroni/mcp9600-python`
* `cd mcp9600-python`
* `sudo ./install.sh --unstable`



# Changelog

0.0.4
-----

* Add set/get for thermocouple type

0.0.3
-----

* Port to i2cdevice>=0.0.6 set/get API

0.0.2
-----

* Added `get_altitude` method
* Corrected pressure to hPa

0.0.1
-----

* Initial Release
