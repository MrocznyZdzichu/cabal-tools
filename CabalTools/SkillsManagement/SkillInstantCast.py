from ..FileHandling.SCPEasyModifier import SCPEasyModifier
import copy

class SkillInstantCast:
    def __init__(self):
        self._scp_processor = SCPEasyModifier()

    def _instant_cast_scps(self, skill_scp, mb_scp, pvp_scp, skill_id, new_value):
        new_scp = self._scp_processor.modify_scp_row(skill_scp, 'SKill_Main', 'SkillIdx', skill_id, 'Instant_Execute', new_value)
        new_mb  = self._scp_processor.modify_scp_row(mb_scp, 'MB_SKill_Main', 'SkillIdx', skill_id, 'Instant_Execute', new_value)
        new_pvp = self._scp_processor.modify_scp_row(pvp_scp, 'PvP_SKill_Main', 'SkillIdx', skill_id, 'Instant_Execute', new_value)

        return new_scp, new_mb, new_pvp

    def _instant_cast_dec(self, skill_dec_data, skill_id, new_value):
        skill_id = str(skill_id)
        new_value = str(new_value)
        updated_dict = copy.deepcopy(skill_dec_data)

        for item in updated_dict.get("children", []):
            if item.get("tag") == "new_skill_list":
                for skill in item.get("children", []):
                    if skill.get("tag") == "skill_main":
                        attributes = skill.get("attributes", {})
                        if attributes.get("id") == skill_id:
                            attributes["instant_execute"] = new_value
                            return updated_dict

        return updated_dict 
    
    def instant_cast(self, skill_dec, skill_scp, mb_scp, pvp_scp, skill_id, new_value):
        new_scp, new_mb, new_pvp = self._instant_cast_scps(skill_scp, mb_scp, pvp_scp, skill_id, new_value)
        new_dec = self._instant_cast_dec(skill_dec, skill_id, new_value)

        return new_dec, new_scp, new_mb, new_pvp