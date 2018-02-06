import datetime
import unittest
import crimereports


TODAY = datetime.datetime.now().date()
NYC = (40.711806, -73.995808)
NEWARK = (40.734985, -74.172447)


class TestDestination(unittest.TestCase):

    def test_destination_miles(self):
        dest = crimereports._destination(NYC, 10, 90, miles=True)
        self.assertAlmostEqual(dest[0], 40.711, delta=0.001)
        self.assertAlmostEqual(dest[1], -73.805, delta=0.001)

    def test_destination_kilometers(self):
        dest = crimereports._destination(NYC, 10, 90, miles=False)
        self.assertAlmostEqual(dest[0], 40.711, delta=0.001)
        self.assertAlmostEqual(dest[1], -73.877, delta=0.001)


class TestCrimeReports(unittest.TestCase):

    def test_incident_transform(self):
        incident = {
            'incident_id': 1,
            'parent_incident_type': 'type',
            'address_1': 'ADDRESS',
            'city': 'CITY',
            'state': 'STATE',
            'incident_description': '10 4, DESC',
            'incident_datetime': '2017-02-02T12:33:00.000',
            'location': {
                'coordinates': [-73.995808, 40.711806]
            }
        }
        self.assertEqual(crimereports._incident_transform(incident), {
            'id': 1,
            'type': 'type',
            'location': 'Address City STATE',
            'description': '10 4, DESC',
            'friendly_description': 'Desc',
            'timestamp': '2017-02-02T12:33:00.000',
            'coordinates': (40.711806, -73.995808)
        })

    def test_validate_incident_types(self):
        with self.assertRaises(ValueError):
            crimereports._validate_incident_types(['Alarm', 'Bad Type'])

    def test_friendly_description(self):
        self.assertEqual(crimereports._friendly_description('10 4, TEST'), 'Test')
        self.assertEqual(crimereports._friendly_description('4 TesT'), 'Test')
        self.assertEqual(crimereports._friendly_description('10 4, TEST, B&E'), 'Test, b&e')

    def test_get_map_url(self):
        cr = crimereports.CrimeReports(NEWARK, 1, miles=True)
        self.assertTrue(cr.get_map_url(TODAY).startswith('https://www.crimereports.com'))

    def test_include(self):
        cr = crimereports.CrimeReports(NEWARK, 1, miles=True)
        url = cr.get_map_url(TODAY, include=['Alarm'])
        self.assertTrue('Alarm' in url)
        self.assertFalse('Assault' in url)

    def test_exclude(self):
        cr = crimereports.CrimeReports(NEWARK, 1, miles=True)
        url = cr.get_map_url(TODAY, exclude=['Alarm'])
        self.assertFalse('Alarm' in url)

    def test_get_incidents(self):
        cr = crimereports.CrimeReports(NEWARK, 0.1, miles=True)
        incidents = cr.get_incidents(TODAY)
        self.assertIsInstance(incidents, list)
