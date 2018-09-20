from runner import CaseRunner
from discord import Client
from client_discord import DiscordTester

Master = CaseRunner()

Discord = DiscordTester("Central-Bot", token="")
Discord.add_casegroups(['cases.skile_bot'])

Master.register_tester(Discord)
Master.run()
