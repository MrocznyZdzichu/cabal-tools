from .ABCSpecificLoader import ABCSpecificLoader


class MobsLoader(ABCSpecificLoader):
    def __init__(self, messages_path):
        super().__init__(messages_path=messages_path, msg_section_start='<mob_msg>', msg_section_end='</mob_msg>')

    def _prepare_confy_mobs_dict(self, raw_mobs_msg):
        return {int(x['id'][len('monster'):]) : x for x in raw_mobs_msg}

    def load(self):
        msg_data  = self._load_msgs()
        msg_data = self._pick_msgs_section(msg_data, r'monster\d+')
        mobs_dict = self._prepare_confy_mobs_dict(msg_data)

        return msg_data, mobs_dict