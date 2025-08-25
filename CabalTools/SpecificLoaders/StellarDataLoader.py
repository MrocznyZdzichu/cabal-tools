from .ABCSpecificLoader import ABCSpecificLoader


class StellarDataLoader(ABCSpecificLoader):
    def __init__(self, scp_path, dec_path, messages_path):
        super().__init__(
            scp_path,
            dec_path,
            messages_path,
            '<stellar_ability>',
            '</stellar_ability>',
            '<stellar_message>',
            '</stellar_message>',
        )

    def load(self):
        scp_data = self._load_scp_file()
        dec_data = self._load_dec()
        msg_data = self._load_msgs()

        return scp_data, dec_data, msg_data
