# bahnapi

## Setup

1. Install `requests` if you haven't already (`pip install requests`).
2. Clone the repository.
3. There's no step 3.

Written for Python 3, but should work in Python 2.

## Usage

```
>>> from bahnapi import Bahn
>>> b = Bahn(key="abc123")
>>> b.find_location("Weimar")
[{'lat': '50.991490', 'lon': '11.326462', 'name': 'Weimar', 'id': '008010366'}, {'lat': '49.349556', 'lon': '8.140757', 'name': 'Neustadt(Weinstr)Hbf', 'id': '008000275'}, {'lat': '52.252218', 'lon': '10.540292', 'name': 'Braunschweig Hbf', 'id': '008000049'}, {'lat': '49.479351', 'lon': '8.468917', 'name': 'Mannheim Hbf', 'id': '008000244'}, {'lat': '52.160627', 'lon': '9.953494', 'name': 'Hildesheim Hbf', 'id': '008000169'}, {'lat': '48.894154', 'lon': '8.703095', 'name': 'Pforzheim Hbf', 'id': '008000299'}, {'lat': '51.431341', 'lon': '6.886510', 'name': 'Mülheim(Ruhr)Hbf', 'id': '008000259'}]
>>> weimar = b.find_location("Weimar")[0]
>>> departures = b.get_departures(weimar)
>>> arrivals = b.get_arrivals(weimar, date="2016-02-29")
>>> journey = b.get_journey(departures[0])
```
