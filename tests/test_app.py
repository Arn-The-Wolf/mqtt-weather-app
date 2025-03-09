import unittest
from server import create_app  # Import the missing function

class TestWeatherStation(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_data_storage(self):
        # Test database operations
        pass

    def test_mqtt_connection(self):
        # Test MQTT connectivity
        pass 