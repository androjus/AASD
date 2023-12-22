#!/usr/bin/env python3
import json
import os

import spade
from spade.agent import Agent
from spade.behaviour import State, FSMBehaviour

STATE_ONE = "STATE_ONE"
STATE_TWO = "STATE_TWO"

class StateOne(State):

    def perform_internal_action(self):
        pass

    async def run(self):
        print("Effector agent at state one")
        self.perform_internal_action()
        self.set_next_state(STATE_ONE)
        msg = await self.receive(timeout=60)
        if msg:
            print(f"Effector agent received request: {msg}")
            if msg.body == STATE_TWO:
                self.set_next_state(STATE_TWO)
                reply = msg.make_reply()
                reply.set_metadata("performative", "agree")
                reply.body = self.next_state
            else:
                reply = msg.make_reply()
                reply.set_metadata("performative", "refuse")
                reply.body = self.next_state
            await self.send(reply)
            

class StateTwo(State):

    def perform_internal_action(self):
        pass

    async def run(self):
        print("Effector agent at state two")
        self.perform_internal_action()
        self.set_next_state(STATE_TWO)
        msg = await self.receive(timeout=60)
        if msg:
            print(f"Effector agent received request: {msg}")
            if msg.body == STATE_ONE:
                self.set_next_state(STATE_ONE)
                reply = msg.make_reply()
                reply.set_metadata("performative", "agree")
                reply.body = self.next_state
            else:
                reply = msg.make_reply()
                reply.set_metadata("performative", "refuse")
                reply.body = self.next_state
            await self.send(reply)

class EffectorAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup(self):
        print(f"Effector agent with id: {self.jid} initialized")
        b = self.FlipFlop()
        b.add_state(name=STATE_ONE, state=StateOne(), initial=True)
        b.add_state(name=STATE_TWO, state=StateTwo())
        b.add_transition(source=STATE_ONE, dest=STATE_TWO)
        b.add_transition(source=STATE_ONE, dest=STATE_ONE)
        b.add_transition(source=STATE_TWO, dest=STATE_ONE)
        b.add_transition(source=STATE_TWO, dest=STATE_TWO)
        template = spade.template.Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(b, template)

    class FlipFlop(FSMBehaviour):
        async def on_start(self):
            print(f"FlipFlop starting at initial state {self.current_state}")
    
        async def on_end(self):
            print(f"FSM finished at state {self.current_state}")
            await self.agent.stop()

async def main():
    effector = EffectorAgent(
        f'{os.environ.get("XMPP_EFFECTOR_NAME")}@{os.environ.get("XMPP_SERVER")}',
        os.environ.get("XMPP_PASSWORD"),
    )
    await effector.start(auto_register=True)
    await spade.wait_until_finished(effector)

if __name__ == "__main__":
    spade.run(main())
