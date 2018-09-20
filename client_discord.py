from discord import Client

from settings import Config
from case import DiscordTestCase, ClientGroup
from exceptions import GroupImportError

import sys
import importlib
import asyncio

class DiscordTester(ClientGroup):
    def __set__(self):
        return set(self)
                   
    def __init__(self, name, *args, **kwargs):
        super().__init__("Discord")
        
        self.__name__ = name
        self.client = Client()
        self.token = kwargs.get("token", None)
        self._config = Config()
        
        self.groups = {}
        self.cases = {}
        
        self._run = self.run
        
    def add_case(self, case: DiscordTestCase):
        self.cases[type(case).__name__] = case
        
    def add_casegroup(self, name: str):
        if name in self.groups:
            raise GroupImportError(f"Requested Group `{name}` is already imported", self)
        
        lib = importlib.import_module(name)
        if not hasattr(lib, "setup"):
            del lib
            del sys.modules[name]
            
            raise GroupImportError(f"Requested Group `{name}` has not the setup function", self)
            
        lib.setup(self)
        self.groups[name] = lib

    def add_casegroups(self, names: list, ignore_error=False):
        _not_loaded = []
        for name in names:
            try:
                self.add_casegroup(name)
            except GroupImportError as ex:
                if ignore_error:
                    _not_loaded.append(name)
                    continue
                else:
                    raise ex
        
        return False if not ignore_error else _not_loaded
    
    def run(self):
        self.result = []
        
        @self.client.event
        async def on_ready():
            for case in self.cases.values():
                _channel = case.target_channel
                _user = case.target_user
                
                channel = self.client.get_channel(_channel)
                user = await self.client.get_user_info(_user)
                
                for command, reaction in case.interaction_data:
                    print(f"Testing case `{command}`, ", end="")
                    await self.client.send_message(channel, command)
                    
                    reply = await self.client.wait_for_message(timeout=3, author=user)
                    if reply.content == reaction.reply:
                        print("Matched")
                    else:
                        print("MisMatched :", reply.content, "(Expected: ", reaction.reply)
                        
                    self.result.append([command, reply.content == reaction.reply])
                        
            await self.client.close()
            
        @self.client.event
        async def on_error(e, *args, **kwargs):
            print("TEARDOWN: Error occured with", repr(e), repr(args), repr(kwargs))
            
            await self.client.close()
            raise sys.exc_info()[1]
        
        # print(dir(self))
        self.client.run(self.token, bot=False)
        
        return {
            "registered": sum(len(v.interaction_data) for v in self.cases.values()),
            "executed": len(self.result),
            "error": sum(1 for c, v in self.result if v == False),
            "data": self.result
        }
