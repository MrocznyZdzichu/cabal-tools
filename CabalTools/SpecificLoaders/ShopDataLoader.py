from .ABCSpecificLoader   import ABCSpecificLoader

class ShopDataLoader(ABCSpecificLoader):
    def __init__(self, npcshop_scp_path, cabal_messages_path):
        super().__init__(
            npcshop_scp_path,
            cabal_messages_path,
            '<cabal_msg>',
            '</cabal_msg>'
        )

    def load(self):
        npcshop_scp_data = self._load_scp_file()
        cabal_messages = self._load_msgs()
        npc_rel_msgs = self._pick_msgs_section(cabal_messages, r'npc\d{2}-\d{4}')

        return npcshop_scp_data, npc_rel_msgs