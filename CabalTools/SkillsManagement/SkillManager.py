from ..ABCBaseManager               import ABCBaseManager

from ..FileHandling.SCPData         import SCPData
from ..FileHandling.XMLSaver        import XMLSaver
from ..FileHandling.SCPPreview      import SCPPreview
from ..FileHandling.SCPxMsgJoiner   import SCPxMsgJoiner

from .SkillDataParser               import SkillDataParser
from .SkillInstantCast              import SkillInstantCast
from .SkillTimeAdjuster             import SkillTimeAdjuster


class SkillManager(ABCBaseManager):
    def __init__(self, scp_data: SCPData, dec_data, msg_data, mb_sc_data: SCPData=None, pvp_scp_data: SCPData =None):
        super().__init__(scp_data, dec_data, msg_data, scp_target_filename='Skill.scp', dec_target_filename='skill.dec')
        self._data_parser       = SkillDataParser()
        self._instant_cast      = SkillInstantCast()
        self._time_adjuster     = SkillTimeAdjuster()

        if mb_sc_data is not None and pvp_scp_data is not None:
            self._skill_mb_data = mb_sc_data
            self._skill_pvp_data = pvp_scp_data

    def _enrich_scp(self):
        skill_scp_with_names = SCPxMsgJoiner().join_scp_with_msg(
            scp           = self._scp_data.data,
            msg           = self._msg_data, 
            scp_key       = 'SkillIdx', 
            key_build_fun = lambda skill_idx: 'skill' + '0' * (4 - len(str(skill_idx))) + str(skill_idx),
            msg_key       = 'id', 
            msg_val       = 'cont',
            new_idx_name  = 'SkillName'
        )
        return skill_scp_with_names

    def save(self, full_save=False):
        super().save()
        if full_save:
            save_config = [
                {'data' : self._skill_mb_data, 'output_Path' : 'MissionBattle.scp'},
                {'data' : self._skill_pvp_data, 'output_Path' : 'PvPBattle.scp'},
            ]
            for conf in save_config:
                conf['data'].save_to_file(conf['output_Path'])

    def instant_cast(self, skill_name, new_value, save_files=True, do_reinit=False):
        skill_id = self._data_parser.get_skill_id(self._msg_data, self._dec_data, skill_name)
        new_dec= self._instant_cast.instant_cast(
            self._dec_data, 
            self._scp_data, 
            self._skill_mb_data, 
            self._skill_pvp_data, 
            skill_id, new_value
        )

        if save_files:
            self.save(full_save=True)

        if do_reinit:
            self.reinit(new_dec=new_dec)
            
        return new_dec
    
    def set_AdjustTime(self, skill_name, new_value, save_files=True, do_reinit=False):
        skill_id = self._data_parser.get_skill_id(self._msg_data, self._dec_data, skill_name)
        
        new_dec = self._time_adjuster.set_skill_AdjustTime(
            skill_id       = skill_id, 
            new_value      = new_value, 
            skill_dec_data = self._dec_data,
            skill_scp_data = self._scp_data
        )

        if save_files:
            self.save()

        if do_reinit:
            self.reinit(new_dec=new_dec)
            
        return new_dec