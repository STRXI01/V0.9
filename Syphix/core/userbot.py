from pyrogram import Client
import asyncio
import config

from ..logging import LOGGER

assistants = []
assistantids = []

class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="Cipher1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )
        self.two = Client(
            name="Cipher2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            name="Cipher3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            name="Cipher4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            name="Cipher5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistants...")
        if config.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat("SyphixHub")
                await self.one.join_chat("Syphixlabs")
            except:
                pass
            assistants.append(1)
            try:
                await self.one.send_message(config.LOG_GROUP_ID, "Assistant Started 1")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 1 has failed to access the log Group."
                )
                exit()
            me = await self.one.get_me()
            self.one.id = me.id
            self.one.name = me.mention
            self.one.username = me.username
            assistantids.append(self.one.id)
            LOGGER(__name__).info(f"Assistant Started as {self.one.name}")

        if config.STRING2:
            await self.two.start()
            try:
                await self.two.join_chat("SyphixHub")
                await self.two.join_chat("Syphixlabs")
            except:
                pass
            assistants.append(2)
            try:
                await self.two.send_message(config.LOG_GROUP_ID, "Assistant Started 2")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 2 has failed to access the log Group."
                )
                exit()
            me = await self.two.get_me()
            self.two.id = me.id
            self.two.name = me.mention
            self.two.username = me.username
            assistantids.append(self.two.id)
            LOGGER(__name__).info(f"Assistant Two Started as {self.two.name}")

        if config.STRING3:
            await self.three.start()
            try:
                await self.three.join_chat("SyphixHub")
                await self.three.join_chat("Syphixlabs")
            except:
                pass
            assistants.append(3)
            try:
                await self.three.send_message(config.LOG_GROUP_ID, "Assistant Started 3")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 3 has failed to access the log Group."
                )
                exit()
            me = await self.three.get_me()
            self.three.id = me.id
            self.three.name = me.mention
            self.three.username = me.username
            assistantids.append(self.three.id)
            LOGGER(__name__).info(f"Assistant Three Started as {self.three.name}")

        if config.STRING4:
            await self.four.start()
            try:
                await self.four.join_chat("SyphixHub")
                await self.four.join_chat("Syphixlabs")
            except:
                pass
            assistants.append(4)
            try:
                await self.four.send_message(config.LOG_GROUP_ID, "Assistant Started 4")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 4 has failed to access the log Group."
                )
                exit()
            me = await self.four.get_me()
            self.four.id = me.id
            self.four.name = me.mention
            self.four.username = me.username
            assistantids.append(self.four.id)
            LOGGER(__name__).info(f"Assistant Four Started as {self.four.name}")

        if config.STRING5:
            await self.five.start()
            try:
                await self.five.join_chat("SyphixHub")
                await self.five.join_chat("Syphixlabs")
            except:
                pass
            assistants.append(5)
            try:
                await self.five.send_message(config.LOG_GROUP_ID, "Assistant Started 5")
            except:
                LOGGER(__name__).error(
                    "Assistant Account 5 has failed to access the log Group."
                )
                exit()
            me = await self.five.get_me()
            self.five.id = me.id
            self.five.name = me.mention
            self.five.username = me.username
            assistantids.append(self.five.id)
            LOGGER(__name__).info(f"Assistant Five Started as {self.five.name}")

    async def stop(self):
        LOGGER(__name__).info(f"Stopping Assistants...")
        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except:
            pass
