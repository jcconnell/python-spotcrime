python-spotcrime [![Build Status](https://travis-ci.org/happyleavesaoc/python-crimereports.svg?branch=master)](https://travis-ci.org/happyleavesaoc/python-crimereports)
==============================================================================================================================================================================================

Provides basic API to [Spot Crime](https://github.com/contra/spotcrime).

## Install

`pip install spotcrime`

## Usage

```python
import datetime
from spotcrime import SpotCrime

sc = SpotCrime((lat, lng), radius, miles=True)
for incident in sc.get_incidents(datetime.datetime.now().date(), None, ['Community Policing']):
  print(incident)
```

## Development

Pull requests welcome. Must pass `tox` and include tests.

## Disclaimer

Not affiliated with spotcrime.com. Use at your own risk.

## NOTES:

These links may be useful in the future:
- http://www.vcso.us/activecalls/
- http://www.volusiasheriff.org/reports/district6-logs.stml
