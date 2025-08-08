from .ABCSpecificLoader   import ABCSpecificLoader

class ItemDataLoader(ABCSpecificLoader):
    def __init__(self, scp_path, messages_path):
        super().__init__(
            scp_path, 
            messages_path, 
            '<item_msg>', 
            '</item_msg>'
        )

    def load(self):
        # scp_data = self._load_scp_file() Item.scp is useless for me so far so it is kept as a mock
        cabal_messages = self._load_msgs()
        item_rel_msgs = self._pick_msgs_section(cabal_messages, r'item\d+')

        return item_rel_msgs