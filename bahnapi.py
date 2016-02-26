from __future__ import print_function
import requests
import json
import datetime


class ApiError(Exception):
    """Generic error type for any error returned by the API."""
    pass


class Bahn(object):
    """Leightweight wrapper for DBOpenData's Fahrplan API."""

    def __init__(self, key=None, lang="de", debug=False):
        if key is None:
            with open("api_key") as f:
                key = f.read().strip()
        self.baseurl = (
                "http://open-api.bahn.de/bin/rest.exe/{}?authKey="
                + key
                + "&lang="
                + lang
                + "&format=json&{}"
                )
        self.debug = debug

    def _request(self, service, args):
        rurl = self.baseurl.format(service, args)
        self.print("GET", rurl)
        r = requests.get(rurl)
        self.print(r.text)
        data = json.loads(r.text)
        self.print(data)
        return data

    def print(self, *args, **kwargs):
        """Print if debug is true"""
        if self.debug:
            print(*args, **kwargs)

    @staticmethod
    def raise_if_necessary(obj):
        if 'errorCode' in obj:
            raise ApiError("{}: {}".format(obj["errorCode"], obj["errorText"]))

    @staticmethod
    def _date_time():
        d = datetime.datetime.now()
        time = d.strftime("%H:%M")
        date = d.strftime("%Y-%M-%d")
        return (date, time)


    def find_location(self, query):
        """Given a query, find a list of matching locations."""
        result = self._request("location.name", "input=" + query)["LocationList"]["StopLocation"]
        # the fuck. "How about we *sometimes* return a list!"
        if isinstance(result, list):
            return result
        return [result]

    def get_departures(self, station_id, date=None, time=None):
        """
        Given a station id (or an element from the list returned by find_location,
        get the next departures for this station.
        """
        if isinstance(station_id, dict):
            station_id = station_id['id']
        date, time = self._date_time()
        db = self._request("departureBoard", "id={}&date={}&time={}".format(
            station_id,
            date,
            time,
            ))["DepartureBoard"]
        self.raise_if_necessary(db)
        result = db["Departure"]
        if isinstance(result, list):
            return result
        return [result]

    def get_arrivals(self, station_id, date=None, time=None):
        """
        Given a station id (or an element from the list returned by find_location,
        get the next arrivals for this station.
        """
        if isinstance(station_id, dict):
            station_id = station_id['id']
        date, time = self._date_time()
        ab = self._request("arrivalBoard", "id={}&date={}&time={}".format(
            station_id,
            date,
            time,
            ))["ArrivalBoard"]
        self.raise_if_necessary(ab)
        result = ab["Arrival"]
        if isinstance(result, list):
            return result
        return [result]

    def get_journey(self, journey):
        """
        Given a journey reference (or a journey from get_arrivals or get_departures,
        return a journey.
        """
        if isinstance(journey, dict):
            journey = journey["JourneyDetailRef"]["ref"]
        jd = self._request("journeyDetail", "ref={}".format(journey))["JourneyDetail"]
        self.raise_if_necessary(jd)
        return jd


if __name__ == '__main__':
    b = Bahn(key=None)  # put API key here
    fra = b.find_location("Frankfurt")[0]
    print(fra)
    dep = b.get_departures(fra)[0]
    print(dep)
    print(b.get_journey(dep))
