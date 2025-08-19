from .ABCSpecificLoader import ABCSpecificLoader


class DropListLoader(ABCSpecificLoader):
    def __init__(self, scp_path=None, dec_path=None, messages_path=None, dec_section_start=None, dec_section_end=None, msg_section_start=None, msg_section_end=None):
        super().__init__(scp_path, dec_path, messages_path, dec_section_start, dec_section_end, msg_section_start, msg_section_end)

    def load(self):
        scp_data = self._load_scp_file()
        return scp_data