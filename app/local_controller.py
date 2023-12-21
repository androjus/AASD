#!/usr/bin/env python3
import json
import os
import time

import spade
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour

STATE_ONE = "STATE_ONE"
STATE_TWO = "STATE_TWO"


class LocalControllerAgent(Agent):
    """queries information from sensor and notifies effector whenever the change of their state is needed"""

    def __init__(
        self, *args, target_temp: tuple[float, float], period: int, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.target_temp = target_temp
        self.period = period
        # TODO: handle state of effectors

    async def setup(self):
        print(f"Local controller agent with id: {self.jid} initialized")
        b = self.ManageEffectors(
            period=self.period, target_temp=self.target_temp
        )
        self.add_behaviour(b)

    class ManageEffectors(PeriodicBehaviour):
        """periodically sends query to sensors, processes results and notifies effectors"""

        def __init__(self, *args, target_temp: tuple[float, float], **kwargs):
            super().__init__(*args, **kwargs)
            self.target_temp = target_temp

        async def run(self):
            print(
                f"Local controller agent with id: {self.agent.jid} querying sensors"
            )
            server_host = self.agent.jid.domain
            msg = spade.message.Message(to=f"sensor@{server_host}")
            msg.set_metadata("performative", "query")
            await self.send(msg)

            # receive all responses from sensors
            responses = await self._get_responses(timeout=2)

            print(
                f"Local controller agent with id: {self.agent.jid} received {len(responses)}"
            )
            print(f"responses: {[resp.body for resp in responses]}")

            if len(responses) == 0:
                return

            # process responses, calculate temperature inside and outside
            avg_temp_out, avg_temp_in = self._process_responses(responses)

            print(
                f"Local controller agent with id: {self.agent.jid} calculated avg temp inside: {avg_temp_in}"
            )
            print(
                f"Local controller agent with id: {self.agent.jid} calculated avg temp outside: {avg_temp_out}"
            )

            # validate current temperature and notify effectors is state change is needed
            if avg_temp_in is None or (
                self.target_temp[0] <= avg_temp_in <= self.target_temp[1]
            ):  # temperature within target, turn off AC, close windows
                await self._send_request_to_effector(
                    to=f"ac@{server_host}", state=STATE_ONE
                )
                await self._send_request_to_effector(
                    to=f"window@{server_host}", state=STATE_ONE
                )
            elif avg_temp_in < self.target_temp[0]:  # temperature too low
                if (
                    avg_temp_out is not None and avg_temp_out > avg_temp_in
                ):  # temperature outside is higher
                    # turn off ac, open windows
                    await self._send_request_to_effector(
                        to=f"ac@{server_host}", state=STATE_ONE
                    )
                    await self._send_request_to_effector(
                        to=f"window@{server_host}", state=STATE_TWO
                    )
                if (
                    avg_temp_out is not None and avg_temp_out < avg_temp_in
                ):  # temperature outside is lower
                    # turn on ac, close windows
                    await self._send_request_to_effector(
                        to=f"ac@{server_host}", state=STATE_TWO
                    )
                    await self._send_request_to_effector(
                        to=f"window@{server_host}", state=STATE_ONE
                    )
            elif avg_temp_in > self.target_temp[1]:  # temperature too high
                if (
                    avg_temp_out is not None and avg_temp_out > avg_temp_in
                ):  # temperature outside is higher
                    # turn on ac, close windows
                    await self._send_request_to_effector(
                        to=f"ac@{server_host}", state=STATE_TWO
                    )
                    await self._send_request_to_effector(
                        to=f"window@{server_host}", state=STATE_ONE
                    )
                if (
                    avg_temp_out is not None and avg_temp_out < avg_temp_in
                ):  # temperature outside is lower
                    # turn off ac, open windows
                    await self._send_request_to_effector(
                        to=f"ac@{server_host}", state=STATE_ONE
                    )
                    await self._send_request_to_effector(
                        to=f"window@{server_host}", state=STATE_TWO
                    )
            else:
                return

            # receive responses from effectors
            await self._get_responses(timeout=2)

        def _process_responses(
            self, responses: list
        ) -> tuple[float | None, float | None]:
            temperatures_with_metadata: list[tuple[float, str]] = [
                (
                    json.loads(resp.body).get("temperature", None),
                    resp.metadata.get("outside", None),
                )
                for resp in responses
            ]

            outside_temperatures = [
                temp
                for temp, outside in temperatures_with_metadata
                if temp is not None
                if outside == "True"
            ]
            inside_temperatures = [
                temp
                for temp, outside in temperatures_with_metadata
                if temp is not None
                if outside == "False"
            ]

            avg_temp_out = (
                sum(outside_temperatures) / len(outside_temperatures)
                if outside_temperatures
                else None
            )
            avg_temp_in = (
                sum(inside_temperatures) / len(inside_temperatures)
                if inside_temperatures
                else None
            )

            return avg_temp_out, avg_temp_in

        async def _send_request_to_effector(self, to: str, state: str) -> None:
            req = spade.message.Message(to=to)
            req.set_metadata("performative", "request")
            req.body = state
            await self.send(req)

        async def _get_responses(self, timeout: int = 10) -> list:
            responses = []
            end_time = time.time() + timeout
            while time.time() < end_time:
                response = await self.receive(timeout=end_time - time.time())
                if response:
                    responses.append(response)
                else:
                    break
            return responses


async def main():
    controller = LocalControllerAgent(
        f'controller@{os.environ.get("XMPP_SERVER")}',
        os.environ.get("XMPP_PASSWORD"),
        target_temp=(20.0, 22.0),
        period=10,
    )
    await controller.start(auto_register=True)
    await spade.wait_until_finished(controller)
    await controller.stop()


if __name__ == "__main__":
    spade.run(main())
