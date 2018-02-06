"""Crime Reports API."""

import calendar
import datetime
import math
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
import requests


DASHBOARD_URL = 'https://www.crimereports.com/home/#!/dashboard'
CRIME_URL = 'https://www.crimereports.com/api/crimes/details.json'
ATTRIBUTION = 'Information provided by spotcrime.com'
SEPARATOR = ','
WHITESPACE = ' '
ATTR_AGENCIES = 'agencies'
ATTR_CRIMES = 'crimes'
HTTP_GET = 'GET'
DAYS = [day.lower() for day in calendar.day_name]  # type: ignore
EARTH_RADIUS = 6378.1
MILES_PER_KILOMETER = 0.621371
UPPER_RIGHT_DEGREE = 45
LOWER_LEFT_DEGREE = 225
INCIDENT_TYPES = ['Alarm', 'Arson', 'Assault', 'Assault with Deadly Weapon',
                  'Breaking & Entering', 'Community Policing', 'Death',
                  'Disorder', 'Drugs', 'Emergency', 'Family Offense', 'Fire',
                  'Homicide', 'Kidnapping', 'Liquor', 'Missing Person', 'Other',
                  'Other Sexual Offense', 'Pedestrian Stop', 'Proactive Policing',
                  'Property Crime', 'Property Crime Commercial',
                  'Property Crime Residential', 'Quality of Life', 'Robbery',
                  'Sexual Assault', 'Sexual Offense', 'Theft', 'Theft from Vehicle',
                  'Theft of Vehicle', 'Traffic', 'Vehicle Recovery', 'Vehicle Stop',
                  'Weapons Offense']


def _destination(start: Tuple[float, float], distance: float,
                 bearing: float, miles: bool=True) -> Tuple[float, float]:
    """Get destination point given a vector (start, distance, bearing)."""
    if miles:
        distance /= MILES_PER_KILOMETER
    lat1 = math.radians(start[0])
    lon1 = math.radians(start[1])
    percent = distance / EARTH_RADIUS
    bearing = math.radians(bearing)
    lat2 = math.asin(math.sin(lat1) * math.cos(percent) +
                     math.cos(lat1) * math.sin(percent) * math.cos(bearing))
    lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(percent) * math.cos(lat1),
                             math.cos(percent) - math.sin(lat1) * math.sin(lat2))
    return (math.degrees(lat2), math.degrees(lon2))


def _incident_transform(incident: Dict[str, Any]) -> Dict[str, Any]:
    """Get output dict from incident."""
    coordinates = None
    if 'location' in incident and 'coordinates' in incident.get('location'):
        coordinates = tuple(incident.get('location').get('coordinates', [])[::-1])
    return {
        'id': incident.get('incident_id'),
        'type': incident.get('parent_incident_type'),
        'description': incident.get('incident_description'),
        'friendly_description': _friendly_description(incident.get('incident_description')),
        'timestamp': incident.get('incident_datetime'),
        'coordinates': coordinates,
        'location': '{} {} {}'.format(incident.get('address_1').capitalize(),
                                      incident.get('city').capitalize(),
                                      incident.get('state'))
    }


def _validate_incident_types(incident_types: Sequence[str]) -> None:
    """Validate an incident types."""
    for incident_type in incident_types:
        if incident_type not in INCIDENT_TYPES:
            raise ValueError('invalid incident type: {}'.format(incident_type))


def _friendly_description(description):
    """Clean up descriptions."""
    clean = []
    for token in description.split():
        if not token.replace(',', '').isdigit():
            clean.append(token.strip())
    return WHITESPACE.join(clean).capitalize()


class SpotCrime():
    """Crime Reports API wrapper."""

    def __init__(self, point: Tuple[float, float], radius: float, miles: bool=False) -> None:
        """Initialize.

        Note that radius implies circular viewport,
        but the Crime Reports API requires a square.
        Therefore, the coordinates sent are the extents
        of a square fit around the circle defined by the
        point and the radius.
        """
        #squared_radius = math.sqrt(2 * math.pow(radius, 2))
        #self._upper_right = _destination(point, squared_radius, UPPER_RIGHT_DEGREE, miles=miles)
        #self._lower_left = _destination(point, squared_radius, LOWER_LEFT_DEGREE, miles=miles)

    def _get_params(self, date: datetime.date, include: Optional[Sequence],
                    exclude: Optional[Sequence]) -> Dict[str, Union[str, int, float]]:
        """HTTP GET request params."""
        incident_types = set(INCIDENT_TYPES)
        if include:
            _validate_incident_types(include)
            incident_types = set(include)
        if exclude:
            _validate_incident_types(exclude)
            incident_types -= set(exclude)
        return {
            'days': SEPARATOR.join(DAYS),
            'end_date': str(date),
            'end_time': 23,
            'incident_types': SEPARATOR.join(incident_types),
            'include_sex_offenders': 'false',
            'filter_by_viewport': 'true',
            'lat1': point[0], #self._upper_right[0],
            'lng1': point[1], #self._upper_right[1],
            #'lat2': self._lower_left[0],
            #'lng2': self._lower_left[1],
            'sandbox': 'false',
            'start_date': str(date),
            'start_time': 0
        }

    def get_map_url(self, date: datetime.date, include: Sequence[str]=None,
                    exclude: Sequence[str]=None) -> str:
        """Get map URL for this instantiation."""
        return requests.Request(HTTP_GET, DASHBOARD_URL,
                                params=self._get_params(lat, lng)).prepare().url
        #return requests.Request(HTTP_GET, DASHBOARD_URL,
                                #params=self._get_params(date, include, exclude)).prepare().url

    def get_incidents(self, date: datetime.date, include: Sequence[str]=None,
                      exclude: Sequence[str]=None) -> List[Dict[str, str]]:
        """Get incidents."""
        resp = requests.get(CRIME_URL, params=self._get_params(date, include, exclude))
        incidents = []  # type: List[Dict[str, str]]
        data = resp.json()
        if ATTR_AGENCIES not in data:
            return incidents
        for agency in data.get(ATTR_AGENCIES):
            for incident in agency.get(ATTR_CRIMES):
                incidents.append(_incident_transform(incident))
        return incidents
