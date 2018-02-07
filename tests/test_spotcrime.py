import datetime
import unittest
import spotcrime


TODAY = datetime.datetime.now().date()
NYC = (40.711806, -73.995808)
NEWARK = (40.734985, -74.172447)


class TestSpotCrime(unittest.TestCase):

    def test_incident_transform(self):
        incident = {
            'incident_id': 1,
            'parent_incident_type': 'type',
            'timestamp': '2017-02-02T12:33:00.000',
            'parent_incident_lat': '-73.995808',
            'parent_incident_lon': '40.711806',
            'location': 'ADDRESS',
            'incident_link': 'https://spotcrime.com/',
        }
        self.assertEqual(spotcrime._incident_transform(incident), {
            'id': 1,
            'type': 'type',
            'timestamp': '2017-02-02T12:33:00.000',
            'lat': '-73.995808',
            'lon': '40.711806',
            'location': 'ADDRESS',
            'link': 'https://spotcrime.com/',
        })

    def test_validate_incident_types(self):
        with self.assertRaises(ValueError):
            crimereports._validate_incident_types(['Alarm', 'Bad Type'])

    def test_get_map_url(self):
        sc = spotcrime.SpotCrime(NEWARK, 0.01)
        self.assertTrue(sc.get_map_url().startswith('https://www.spotcrime.com'))

    def test_get_incidents(self):
        sc = spotcrime.SpotCrime(NEWARK, 0.01)
        incidents = sc.get_incidents()
        self.assertIsInstance(incidents, list)
