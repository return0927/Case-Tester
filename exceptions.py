class GroupImportError(Exception):
    """Error occured when importing a group of testcases
    """
    def __init__(self, error, raiser, data=None):
        super().__init__(error)
        self.raiser = raiser
        self.data = data

class ClientImportError(Exception):
    """Error occured when importing a client group
    """
    def __init__(self, error, raiser, data=None):
        super().__init__(error)
        self.raiser = raiser
        self.data = data


        