import unittest
from unittest.mock import MagicMock, AsyncMock
from agents.controller.local_controller import LocalControllerAgent, STATE_ONE

class TestLocalControllerAgent(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.agent = LocalControllerAgent(
            "controller@localhost", "password", target_temp=(20.0, 22.0), period=10
        )
        self.agent.send = MagicMock()
        self.agent.stop = AsyncMock()

    async def asyncTearDown(self):
        await self.agent.stop()

    async def test_process_responses(self):
        responses = [
            MagicMock(body='{"temperature": 22}', metadata={'outside': 'True'}),
            MagicMock(body='{"temperature": 21}', metadata={'outside': 'False'}),
            MagicMock(body='{"temperature": 18}', metadata={'outside': 'True'}),
        ]

        avg_temp_out, avg_temp_in = self.agent.ManageEffectors._process_responses(self.agent.ManageEffectors, responses)

        self.assertAlmostEqual(avg_temp_out, (22 + 18) / 2)
        self.assertAlmostEqual(avg_temp_in, 21)


if __name__ == '__main__':
    unittest.main()