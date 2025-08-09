from ..FileHandling.SCPEasyModifier import SCPEasyModifier
import copy


class SkillTimeAdjuster:
    def __init__(self):
        self._scp_processor = SCPEasyModifier()

    def _set_AdjustTime_scp(self, skill_scp_data, skill_id, new_value):
        return self._scp_processor.modify_scp(
            scp_data       = skill_scp_data,
            section_name   = 'SKill_Main',
            item_key_field = 'SkillIdx', 
            item_key_value = skill_id, 
            field_name     = 'AdjustTime', 
            new_value      = new_value
        )

    def _set_AdjustTime_dec(self, skill_id, new_value, skill_dec_data):
        skill_id = str(skill_id)
        new_value = str(new_value)
        updated_dict = copy.deepcopy(skill_dec_data)

        for item in updated_dict.get("children", []):
            if item.get("tag") == "new_skill_list":
                for skill in item.get("children", []):
                    if skill.get("tag") == "skill_main":
                        attributes = skill.get("attributes", {})
                        if attributes.get("id") == skill_id:
                            attributes["AdjustTime"] = new_value
                            return updated_dict

        return updated_dict 

    def set_skill_AdjustTime(self, skill_id, new_value, skill_dec_data, skill_scp_data):
        new_scp = self._set_AdjustTime_scp(
            skill_scp_data = skill_scp_data, 
            skill_id       = skill_id, 
            new_value      = new_value
        )
        new_dec = self._set_AdjustTime_dec(
            skill_id       = skill_id, 
            new_value      = new_value, 
            skill_dec_data = skill_dec_data
        )

        return new_dec, new_scp