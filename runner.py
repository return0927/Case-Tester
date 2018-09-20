from case import ClientGroup
from exceptions import ClientImportError


class CaseRunner:
    testers = set()
    
    @classmethod
    def get_testers(self):
        return [*self.testers]
    
    def __init__(self, **kwargs):
        self.testers = kwargs.get("testers", self.testers)
        
    def register_tester(self, tester):
        if not issubclass(tester.__class__, ClientGroup):
            raise ClientImportError(f"Requested `{repr(tester)}` is not a valid tester", self, {"requested_argument": tester})
        self.testers.add(tester)
        
    def run(self):
        for tester in self.testers:
            print(type(tester).__name__, tester.run())

