from pyrogram import Client
import asyncio
import config
from ..logging import LOGGER

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        configs = [
            (1, "AMBOTAss1", config.STRING1),
            (2, "AMBOTAss2", config.STRING2),
            (3, "AMBOTAss3", config.STRING3),
            (4, "AMBOTAss4", config.STRING4),
            (5, "AMBOTAss5", config.STRING5),
        ]
        self.clients = {}
        for num, name, string in configs:
            if string:
                self.clients[num] = Client(
                    name=name,
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    session_string=str(string),
                    no_updates=True,
                )

    async def start(self):
        LOGGER(__name__).info("Starting Assistants...")
        for num, client in self.clients.items():
            await client.start()
            try:
                await client.join_chat("SyphixHub")
                await client.join_chat("Syphixlabs")
            except:
                pass
            assistants.append(num)
            try:
                await client.send_message(config.LOG_GROUP_ID, f"Assistant Started {num}")
            except:
                LOGGER(__name__).error(
                    f"Assistant Account {num} has failed to access the log Group. "
                    "Make sure that you have added your assistant to your log group and promoted as admin!"
                )
                exit()
            me = await client.get_me()
            client.id = me.id
            client.name = me.mention
            client.username = me.username
            assistantids.append(client.id)
            LOGGER(__name__).info(f"Assistant {num} Started as {client.name}")

    async def stop(self):
        LOGGER(__name__).info("Stopping Assistants...")
        for client in self.clients.values():
            try:
                await client.stop()
            except:
                pass