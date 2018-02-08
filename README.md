python-spotcrime [![Build Status](https://travis-ci.org/jcconnell/python-spotcrime.svg?branch=master)](https://travis-ci.org/jcconnell/python-spotcrime)
==============================================================================================================================================================================================

Provides basic API to [Spot Crime](https://spotcrime.com/).

## Install

`pip install spotcrime`

## Usage

```python
from spotcrime import SpotCrime

sc = SpotCrime((lat, lng), radius)
for incident in sc.get_incidents():
  print(incident)
```

## Development

Pull requests welcome.

## Disclaimer

Not affiliated with spotcrime.com. Use at your own risk.

## TODO:
- Smarter radius conversion (1 mile = 0.01)
- Support included/excluded types
- Support date ranges

## NOTES:

These links may be useful in the future:
- http://www.vcso.us/activecalls/
- http://www.volusiasheriff.org/reports/district6-logs.stml
