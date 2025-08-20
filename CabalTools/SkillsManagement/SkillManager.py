from ..FileHandling.SCPData         import SCPData
from ..FileHandling.XMLSaver        import XMLSaver
from ..FileHandling.SCPPreview      import SCPPreview
from ..FileHandling.SCPxMsgJoiner   import SCPxMsgJoiner

from .SkillDataParser               import SkillDataParser
from .SkillInstantCast              import SkillInstantCast
from .SkillTimeAdjuster             import SkillTimeAdjuster


class SkillManager:
    def __init__(self, skill_names, skill_details, skill_scp_data: SCPData, mb_sc_data: SCPData=None, pvp_scp_data: SCPData =None):
        self._data_parser       = SkillDataParser()
        self._skill_names       = skill_names
        self._skill_details     = skill_details
        self._skill_scp_data    = skill_scp_data
        self._skill_rich_data   = self._enrich_skills_scp()

        self._instant_cast      = SkillInstantCast()
        self._time_adjuster     = SkillTimeAdjuster()

        if mb_sc_data is not None and pvp_scp_data is not None:
            self._skill_mb_data = mb_sc_data
            self._skill_pvp_data = pvp_scp_data

    def reinit(self, new_skill_details):
        self._skill_details   = new_skill_details
        self._skill_rich_data = self._enrich_skills_scp()

    def _enrich_skills_scp(self):
        skill_scp_with_names = SCPxMsgJoiner().join_scp_with_msg(
            scp           = self._skill_scp_data.data,
            msg           = self._skill_names, 
            scp_key       = 'SkillIdx', 
            key_build_fun = lambda skill_idx: 'skill' + '0' * (4 - len(str(skill_idx))) + str(skill_idx),
            msg_key       = 'id', 
            msg_val       = 'cont',
            new_idx_name  = 'SkillName'
        )
        return skill_scp_with_names

    def skill_preview(self, section_name=None, columns=None, filter_key=None, filter_val=None, filter_operator=None):
        SCPPreview().preview(
            self._skill_rich_data, 
            section_name, 
            columns, 
            filter_key, 
            filter_val,
            filter_operator
        )

    def instant_cast(self, skill_name, new_value, save_files=True, do_reinit=False):
        skill_id = self._data_parser.get_skill_id(self._skill_names, self._skill_details, skill_name)
        new_dec= self._instant_cast.instant_cast(
            self._skill_details, 
            self._skill_scp_data, 
            self._skill_mb_data, 
            self._skill_pvp_data, 
            skill_id, new_value
        )

        if save_files:
            save_config = [
                {'data' : self._skill_scp_data, 'output_Path' : 'Skill.scp'},
                {'data' : self._skill_mb_data, 'output_Path' : 'MissionBattle.scp'},
                {'data' : self._skill_pvp_data, 'output_Path' : 'PvPBattle.scp'},
            ]
            for conf in save_config:
                conf['data'].save_to_file(conf['output_Path'])
            XMLSaver().save_dict_to_file(new_dec, 'skill.dec')

        if do_reinit:
            self.reinit(new_dec)
            
        return new_dec
    
    def set_AdjustTime(self, skill_name, new_value, save_files=True, do_reinit=False):
        skill_id = self._data_parser.get_skill_id(self._skill_names, self._skill_details, skill_name)
        
        new_dec = self._time_adjuster.set_skill_AdjustTime(
            skill_id       = skill_id, 
            new_value      = new_value, 
            skill_dec_data = self._skill_details,
            skill_scp_data = self._skill_scp_data
        )

        if save_files:
            self._skill_scp_data.save_to_file('Skill.scp')
            XMLSaver().save_dict_to_file(new_dec, 'skill.dec')

        if do_reinit:
            self.reinit(new_dec)
            
        return new_dec