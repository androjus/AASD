import unittest
from agents.monitor.monitor_terminal import MonitorAgent
from agents.sensor.sensor import SensorAgent

class TestMonitorAgent(unittest.TestCase):
    def setUp(self):
        _ = SensorAgent(
            "sensor@localhost",
            "test_password",
            outside=True,
        )
        self.monitor_agent = MonitorAgent(
            "monitor@localhost",
            "test_password"
        )

    def test_monitor_agent_initialization(self):
        self.assertEqual(self.monitor_agent.jid.localpart, "monitor")
        self.assertEqual(self.monitor_agent.jid.domain, "localhost")

if __name__ == '__main__':
    unittest.main()
