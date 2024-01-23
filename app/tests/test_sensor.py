import unittest
from unittest.mock import patch, MagicMock
from agents.sensor.sensor import SensorAgent
import json

class TestSensorAgent(unittest.TestCase):
    @patch('spade.agent.Agent')
    def setUp(self, mock_agent):
        self.sensor_agent = SensorAgent('sensor@localhost', 'password', outside=True)
        self.sensor_agent.start = MagicMock()

    def test_init(self):
        self.assertEqual(self.sensor_agent.jid.localpart, 'sensor')
        self.assertEqual(self.sensor_agent.jid.domain, 'localhost')
        self.assertTrue(self.sensor_agent.outside)

    @patch('spade.behaviour.CyclicBehaviour')
    def test_measure_value(self, mock_cyclic_behaviour):
        measure_value = self.sensor_agent.MeasureValue(outside=True)
        self.assertTrue(measure_value.outside)

    def test_get_readings(self):
        measure_value = self.sensor_agent.MeasureValue(outside=True)
        readings = measure_value._get_readings()
        self.assertTrue(5 <= json.loads(readings)["temperature"] <= 30)

if __name__ == '__main__':
    unittest.main()
