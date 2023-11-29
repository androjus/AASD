#!/usr/bin/env python3
import os
import spade

class DummyAgent(spade.agent.Agent):
    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))

async def main():
    dummy = DummyAgent(
        f'your_jid@{os.environ.get("XMPP_SERVER")}', os.environ.get("XMPP_PASSWORD")
    )
    await dummy.start()

if __name__ == "__main__":
    spade.run(main())