from case import DiscordTestCase, Reaction


class SkileBot(DiscordTestCase):
    target_channel = "274134846216077314"
    target_user = "405664776954576896"

skile = SkileBot()
skile.append_interaction("히익", Reaction(reply="힉"))

def setup(tester):
    tester.add_case(skile)
