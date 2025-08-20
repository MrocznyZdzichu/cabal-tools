from .ABCSpecificLoader import ABCSpecificLoader


class MultipleSCPLoader(ABCSpecificLoader):
    def __init__(self, scp_path):
        super().__init__(scp_path=scp_path)

    def load(self):
        return self._load_scp_file()