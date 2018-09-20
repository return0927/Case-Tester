class Reaction:
    def __dict__(self):
        return {"reply": self.reply, "reaction": self.reaction}
    
    def __repr__(self):
        return repr(self.__dict__())
        
    def __init__(self, **kwargs):
        self.reply = kwargs.get("reply", None)
        self.reaction = kwargs.get("reaction", None)


class DiscordTestCase:
    target_channel = None
    target_user = None
        
    interaction_data = []
    
    @classmethod
    def get_destination(self):
        return {"channel": self.target_channel, "user": self.target_user}
        
    def append_interaction(self, testMessage, reaction: Reaction):
        self.interaction_data.append(
            [
                testMessage,
                reaction
            ]
        )

    def run(self):
        return True

    
class ClientGroup:
    def __init__(self, platform):
        self.platform = platform
        
        self.cases = {}

    def run(self):
        return {
            "registered": 0,
            "executed": 0,
            "error": 0,
            "data": []
        }
        