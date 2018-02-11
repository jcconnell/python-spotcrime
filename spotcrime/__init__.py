"""Spot Crime API."""

from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
import requests
import datetime


CRIME_URL = 'http://api.spotcrime.com/crimes.json'
DASHBOARD_URL = 'https://spotcrime.com/'
API_KEY = 'privatekeyforspotcrimepublicusers-commercialuse-877.410.1607'
USER_AGENT = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
ATTRIBUTION = 'Information provided by spotcrime.com'
ATTR_CRIMES = 'crimes'
HTTP_GET = 'GET'
INCIDENT_TYPES = ['Arrest', 'Arson', 'Assault', 'Burglary', 'Robbery', 'Shooting',
        'Theft', 'Vandalism', 'Other']


def _validate_incident_date_range(incident, numdays):
    """Returns true if incident is within date range"""
    try:
        datetime_object = datetime.datetime.strptime(incident.get('date'), '%m/%d/%y %I:%M %p')
    except ValueError:
        raise ValueError("Incorrect date format, should be MM/DD/YY HH:MM AM/PM")
    timedelta = datetime.timedelta(days=numdays)
    today = datetime.datetime.now()
    if today - datetime_object <= timedelta:
        return True
    return False

def _incident_transform(incident):
    """Get output dict from incident."""
    return {
        'id': incident.get('cdid'),
        'type': incident.get('type'),
        'timestamp': incident.get('date'),
        'lat': incident.get('lat'),
        'lon': incident.get('lon'),
        'location': incident.get('address'),
        'link': incident.get('link')
    }

class SpotCrime():
    """Spot Crime API wrapper."""

    def __init__(self, point, rad, days=1):
        self.point = point #tuple
        self.rad = rad #float
        self.days = days #int
        self.headers = {
            'User-Agent': USER_AGENT
        }

    def _get_params(self):
        return {
            'key': API_KEY,
            'lat': self.point[0],
            'lon': self.point[1],
            'radius': self.rad
        }

    def get_map_url(self):
        """Get map URL for this instantiation."""
        return requests.Request(HTTP_GET, DASHBOARD_URL).prepare().url

    def get_incidents(self):
        """Get incidents."""
        resp = requests.get(CRIME_URL, params=self._get_params(), headers=self.headers)
        incidents = []  # type: List[Dict[str, str]]
        data = resp.json()
        if ATTR_CRIMES not in data:
            return incidents
        for incident in data.get(ATTR_CRIMES):
            if _validate_incident_date_range(incident, self.days):
                incidents.append(_incident_transform(incident))
        return incidents
