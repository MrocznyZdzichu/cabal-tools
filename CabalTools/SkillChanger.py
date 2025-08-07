from .SkillDataParser   import SkillDataParser
from .SCPSaver          import SCPSaver
from .XMLSaver          import XMLSaver
from .SCPEasyModifier   import SCPEasyModifier

from .SkillInstantCast  import SkillInstantCast

import copy


class SkillChanger:
    def __init__(self, skill_names, skill_details, skill_scp_data, mb_sc_data=None, pvp_scp_data=None):
        self._data_parser       = SkillDataParser()
        self._instant_cast      = SkillInstantCast()
        self._skill_names       = skill_names
        self._skill_details     = skill_details
        self._skill_scp_data    = skill_scp_data

        if mb_sc_data is not None and pvp_scp_data is not None:
            self._skill_mb_data = mb_sc_data
            self._skill_pvp_data = pvp_scp_data

    def reinit(self, new_skill_details, new_skill_scp_data, new_skill_mb_data=None, new_skill_pvp_data=None):
        self._skill_details = new_skill_details
        self._skill_scp_data = new_skill_scp_data

        if new_skill_mb_data is not None and new_skill_pvp_data is not None:
            self._skill_mb_data = new_skill_mb_data
            self._skill_pvp_data = new_skill_pvp_data

 
    def instant_cast(self, skill_name, new_value, save_files=True, do_reinit=False):
        skill_id = self._data_parser.get_skill_id(self._skill_names, self._skill_details, skill_name)
        new_dec, new_scp, new_mb, new_pvp = self._instant_cast.instant_cast(self._skill_details, 
                                                                            self._skill_scp_data, 
                                                                            self._skill_mb_data, 
                                                                            self._skill_pvp_data, 
                                                                            skill_id, new_value
        )

        if save_files:
            scp_saver = SCPSaver()
            scp_saver.save_scp_file(new_scp, 'Skill.scp')
            scp_saver.save_scp_file(new_mb, 'MissionBattle.scp')
            scp_saver.save_scp_file(new_pvp, 'PvPBattle.scp')
            XMLSaver().save_dict_to_file(new_dec, 'skill.dec')

        if do_reinit:
            self.reinit(new_dec, new_scp, new_mb, new_pvp)
            
        return new_scp, new_dec
    