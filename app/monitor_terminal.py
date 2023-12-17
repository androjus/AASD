#!/usr/bin/env python3
import os
import time

import spade
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour

class MonitorAgent(Agent):
    '''periodically sends query messages to all sensors'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def setup(self):
        print(f"Monitor agent with id: {self.jid} initialized")
        b = self.SendQuery(period=5)
        self.add_behaviour(b)
    
    class SendQuery(PeriodicBehaviour):
        async def run(self):
            print(f"Monitor agent with id: {self.agent.jid} querying sensors")
            server_host = self.agent.jid.domain
            msg = spade.message.Message(to=f"sensor@{server_host}")
            msg.set_metadata("performative", "query")
            await self.send(msg)

            #receive all responses
            responses = []
            responses_timeout = 2
            end_time = time.time() + responses_timeout
            while time.time() < end_time:
                response = await self.receive(timeout=end_time - time.time())
                if response:
                    responses.append(response)
                else:
                    break
                        
            print(f"Monitor agent with id: {self.agent.jid} received {len(responses)}")
            print(f"responses: {[resp.body for resp in responses]}")

async def main():
    monitor = MonitorAgent(
        f'monitor@{os.environ.get("XMPP_SERVER")}',
        os.environ.get("XMPP_PASSWORD"),
    )
    await monitor.start(auto_register=True)
    await spade.wait_until_finished(monitor)

if __name__ == "__main__":
    spade.run(main())
