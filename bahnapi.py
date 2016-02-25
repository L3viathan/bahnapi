from __future__ import print_function
import requests
import json
import datetime


class ApiError(Exception):
    """Generic error type for any error returned by the API."""
    pass


class Bahn(object):
    """Leightweight wrapper for DBOpenData's Fahrplan API."""

    def __init__(self, key=None, lang="de"):
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

    def _request(self, service, args):
        rurl = self.baseurl.format(service, args)
        print("GET", rurl)
        r = requests.get(rurl)
        return json.loads(r.text)

    @staticmethod
    def _date_time():
        d = datetime.datetime.now()
        time = d.strftime("%H:%M")
        date = d.strftime("%Y-%M-%d")
        return (date, time)


    def find_location(self, query):
        """Given a query, find a list of matching locations."""
        return self._request("location.name", "input=" + query)["LocationList"]["StopLocation"]

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
        if 'errorCode' in db:
            raise ApiError("{}: {}".format(db["errorCode"], db["errorText"]))
        return db["Departure"]

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
        if 'errorCode' in ab:
            raise ApiError("{}: {}".format(ab["errorCode"], ab["errorText"]))
        return ab["Arrival"]

    def get_journey(self, journey):
        """
        Given a journey reference (or a journey from get_arrivals or get_departures,
        return a journey.
        """
        if isistance(journey, dict):
            journey = journey["JourneyRef"]["ref"]
        return self._request("journeyDetail", "ref={}".format(journey))


if __name__ == '__main__':
    b = Bahn(key=None)  # put API key here
    fra = b.find_location("Frankfurt")[0]
    print(fra)
    dep = b.get_departures(fra)
    print(dep)
    print(b.get_journey(dep))
