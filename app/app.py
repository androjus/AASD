import os
import spade

class DummyAgent(spade.agent.Agent):
    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))

async def main():
    dummy = DummyAgent(
        f'test23@{os.environ.get("XMPP_SERVER")}',
        os.environ.get("XMPP_PASSWORD")
    )
    await dummy.start(auto_register=True)

if __name__ == "__main__":
    spade.run(main())