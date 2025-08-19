from .ABCSpecificLoader import ABCSpecificLoader


class ConstSCPLoader(ABCSpecificLoader):
    def __init__(self, scp_path):
        super().__init__(
            scp_path=scp_path, 
            dec_path=None, 
            messages_path=None, 
            dec_section_start=None, 
            dec_section_end=None, 
            msg_section_start=None, 
            msg_section_end=None
        )

    def load(self):
        return self._load_scp_file()