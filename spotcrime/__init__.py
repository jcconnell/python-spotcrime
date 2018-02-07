"""Spot Crime API."""

import calendar
import datetime
import math
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
import requests

CRIME_URL = 'http://api.spotcrime.com/crimes.json'
DASHBOARD_URL = 'https://spotcrime.com/'
API_KEY = 'privatekeyforspotcrimepublicusers-commercialuse-877.410.1607'
USER_AGENT = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
ATTRIBUTION = 'Information provided by spotcrime.com'
SEPARATOR = ','
WHITESPACE = ' '
ATTR_CRIMES = 'crimes'
HTTP_GET = 'GET'
INCIDENT_TYPES = ['Arrest', 'Arson', 'Assault', 'Burglary', 'Robbery', 'Shooting',
        'Theft', 'Vandalism', 'Other']

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


def _validate_incident_types(incident_types: Sequence[str]) -> None:
    """Validate an incident types."""
    for incident_type in incident_types:
        if incident_type not in INCIDENT_TYPES:
            raise ValueError('invalid incident type: {}'.format(incident_type))


class SpotCrime():
    """Crime Reports API wrapper."""

    def __init__(self, point, rad):
        self.point = point #tuple
        self.rad = rad #float
        self.headers = {
            'User-Agent': USER_AGENT
        }
        pass

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

    def get_incidents(self, date: datetime.date, include: Sequence[str]=None,
                      exclude: Sequence[str]=None) -> List[Dict[str, str]]:
        """Get incidents."""
        resp = requests.get(CRIME_URL, params=self._get_params(), headers=self.headers)
        incidents = []  # type: List[Dict[str, str]]
        data = resp.json()
        if ATTR_CRIMES not in data:
            return incidents
        for incident in data.get(ATTR_CRIMES):
            incidents.append(_incident_transform(incident))
        return incidents
