import unittest
from unittest.mock import MagicMock
from spade.message import Message
from agents.effector.effector import EffectorAgent, STATE_ONE, STATE_TWO

class TestEffectorAgent(unittest.TestCase):

    def setUp(self):
        self.agent = EffectorAgent("effector@localhost", "password")
        self.agent.send = MagicMock()
        self.agent.stop = MagicMock()

    def test_state_transitions(self):

        self.agent.FlipFlop.current_state = STATE_ONE
        self.assertEqual(self.agent.FlipFlop.current_state, STATE_ONE)

        self.agent.send.reset_mock()
        self.agent.FlipFlop.current_state = STATE_TWO
        self.assertEqual(self.agent.FlipFlop.current_state, STATE_TWO)

    def test_message_handling(self):
        self.agent.FlipFlop.current_state = STATE_ONE
        self.agent.receive = MagicMock(return_value=Message(to=str(self.agent.jid), body=STATE_TWO))
        self.assertEqual(self.agent.FlipFlop.current_state, STATE_ONE)

        self.agent.send.reset_mock()
        self.agent.FlipFlop.current_state = STATE_TWO
        self.agent.receive = MagicMock(return_value=Message(to=str(self.agent.jid), body=STATE_ONE))
        self.assertEqual(self.agent.FlipFlop.current_state, STATE_TWO)

if __name__ == '__main__':
    unittest.main()