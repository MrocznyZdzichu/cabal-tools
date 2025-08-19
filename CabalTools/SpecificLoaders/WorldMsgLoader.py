import copy

from .ABCSpecificLoader import ABCSpecificLoader


class WorldMsgLoader(ABCSpecificLoader):
    def __init__(self, messages_path):
        super().__init__(
            messages_path     = messages_path, 
            msg_section_start = '<cabal_msg>', 
            msg_section_end   = '</cabal_msg>'
        )

    def _prepare_comfy_dict(self, raw_msg):
        return {int(x['id'][len('world'):]) : x for x in raw_msg}

    def load(self):
        msg_data = self._load_msgs()
        msg_data = self._pick_msgs_section(msg_data, r'world\d+')
        world_ids_dict = self._prepare_comfy_dict(msg_data)
        return msg_data, world_ids_dict