#!/usr/bin/env python3
import json
import os

import spade
from spade.agent import Agent
from spade.behaviour import State


class EffectorAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup(self):
        print(f"Effector agent with id: {self.jid} initialized")
        b = self.FlipFlop()
        template = spade.template.Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(b, template)

    class FlipFlop(State):
        """responds to request with agree/cancel and state in msg.body"""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def perform_internal_action(self, state):
            pass

        def change_state(self, state):
            self.set_next_state(state)
            self.perform_internal_action(state)
            print(f"Effector agent changed state to: {self.next_state}")  

        async def run(self):
            msg = await self.receive()
            if msg:
                print(f"Effector agent received request: {msg}")
                if msg.body != self.next_state:
                    self.change_state(msg.body)
                    reply = msg.make_reply()
                    reply.set_metadata("performative", "agree")
                    reply.body = self.next_state
                else:
                    reply = msg.make_reply()
                    reply.set_metadata("performative", "cancel")
                    reply.body = self.next_state
                await self.send(reply)

async def main():
    effector = EffectorAgent(
        f'effector@{os.environ.get("XMPP_SERVER")}',
        os.environ.get("XMPP_PASSWORD"),
    )
    await effector.start(auto_register=True)
    await spade.wait_until_finished(effector)



if __name__ == "__main__":
    spade.run(main())
