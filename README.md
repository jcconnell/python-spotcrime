python-spotcrime [![Build Status](https://travis-ci.org/jcconnell/python-spotcrime.svg?branch=master)](https://travis-ci.org/jcconnell/python-spotcrime)
==============================================================================================================================================================================================

Provides basic API to [Spot Crime](https://spotcrime.com/).

## Install

`pip install spotcrime`

## Usage

```python
from spotcrime import SpotCrime

sc = SpotCrime((lat, lng), radius, None, ['Other'], "your-api-key", days=10)
for incident in sc.get_incidents():
  print(incident)
```

## Development

Pull requests welcome.

## Disclaimer

Not affiliated with spotcrime.com. Use at your own risk.

## TODO:
- Smarter radius conversion (1 mile = 0.01)
- ~~Support included/excluded types~~
- ~~Support date ranges~~

## NOTES:

To obtain an API key for commercial or research use, please contact 877.410.1607 or pyrrhus-at-spotcrime.com. The maximum number of returned results is 50, regardless of date.
