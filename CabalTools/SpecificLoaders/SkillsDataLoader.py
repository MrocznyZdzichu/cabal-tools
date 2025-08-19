from .ABCSpecificLoader import ABCSpecificLoader

class SkillsDataLoader(ABCSpecificLoader):
    def __init__(self, skill_dec_path, cabal_msg_path, skill_scp_path,
                 skill_mb_path=None, skill_pvp_path=None):
        super().__init__(
            scp_path=skill_scp_path, 
            dec_path=skill_dec_path, 
            messages_path=cabal_msg_path, 
            dec_section_start='<cabal_skill>', 
            dec_section_end='</cabal_skill>',
            msg_section_start='<cabal_msg>', 
            msg_section_end='</cabal_msg>'
        )
        self._skill_mb_path = skill_mb_path
        self._skill_pvp_path = skill_pvp_path

    def load(self):
        cabal_messages = self._load_msgs()
        cabal_skill_names = self._pick_msgs_section(cabal_messages, r'skill\d+')
        skill_dec_data = self._load_dec()
        skill_scp_data = self._load_scp_file()

        if self._skill_mb_path and self._skill_pvp_path:
            skill_mb_data = self._scp_loader.load_scp_file(self._skill_mb_path)
            skill_pvp_data = self._scp_loader.load_scp_file(self._skill_pvp_path)
            return cabal_skill_names, skill_dec_data, skill_scp_data, skill_mb_data, skill_pvp_data

        return cabal_skill_names, skill_dec_data, skill_scp_data