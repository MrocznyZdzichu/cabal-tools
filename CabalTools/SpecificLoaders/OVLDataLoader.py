from .ABCSpecificLoader import ABCSpecificLoader


class OVLDataLoader(ABCSpecificLoader):

    def __init__(self, scp_path, dec_path, messages_path):
        super().__init__(
            scp_path,
            dec_path,
            messages_path,
            dec_section_start='<overloadmastery_system>',
            dec_section_end='</overloadmastery_system>',
            msg_section_start='<overloadmastery_message>',
            msg_section_end='</overloadmastery_message>',
        )

    def load(self):
        scp_data = self._load_scp_file()
        dec_data = self._load_dec()
        msg_data = self._load_msgs()

        return scp_data, dec_data, msg_data