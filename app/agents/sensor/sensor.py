#!/usr/bin/env python3
import json
import os

import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour


class SensorAgent(Agent):
    def __init__(self, *args, outside: bool, **kwargs):
        super().__init__(*args, **kwargs)
        self.outside = outside
        #TODO other parameters like rain, wind, etc.

        #Mock tempature generating
        self._last_tempature = 10
        self._temp_growing = True

    async def setup(self):
        print(f"Sensor agent with id: {self.jid} initialized")
        b = self.MeasureValue(outside=self.outside)
        template = spade.template.Template()
        template.set_metadata("performative", "query")
        self.add_behaviour(b, template)

    class MeasureValue(CyclicBehaviour):
        """responds to query with measurement"""

        def __init__(self, outside: bool, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.outside = outside

        async def run(self):
            msg = await self.receive()
            if msg:
                print(f"Sensor agent received query: {msg}")
                reply = msg.make_reply()
                reply.set_metadata("outside", str(self.outside))
                reply.set_metadata("performative", "inform")
                reply.body = self._get_readings()
                await self.send(reply)
        
        def _get_readings(self) -> str:
            results = {}
            results["temperature"] = self._generate_tempature()
            return json.dumps(results)
        
        def _generate_tempature(self) -> int:
            MIN_TEMP = 5
            MAX_TEMP = 30
            if self._temp_growing:
                self._last_tempature += 1
                if self._last_tempature >= MAX_TEMP:
                    self._temp_growing = False
            else:
                self._last_tempature -= 1
                if self._last_tempature <= MIN_TEMP:
                    self._temp_growing = True
            return self._last_tempature

            

async def main():
    sensor = SensorAgent(
        f'{os.environ.get("XMPP_SENSOR_NAME")}@{os.environ.get("XMPP_SERVER")}',
        os.environ.get("XMPP_PASSWORD"),
        outside=True
    )
    await sensor.start(auto_register=True)
    await spade.wait_until_finished(sensor)



if __name__ == "__main__":
    spade.run(main())
