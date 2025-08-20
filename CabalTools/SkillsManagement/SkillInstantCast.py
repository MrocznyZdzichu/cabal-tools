import copy

# from ..FileHandling.SCPEasyModifier import SCPEasyModifier
from ..FileHandling.SCPData         import SCPData


class SkillInstantCast:
    def __init__(self):
        pass

    def _instant_cast_scps(self, skill_scp: SCPData, mb_scp: SCPData, pvp_scp: SCPData, skill_id, new_value):
        process_map = [
            {'scp' : skill_scp, 'section_name' : 'SKill_Main'},
            {'scp' : mb_scp,    'section_name' : 'MB_SKill_Main'},
            {'scp' : pvp_scp,   'section_name' : 'PvP_SKill_Main'}
        ]

        for conf in process_map:
            conf['scp'].modify_field(
                section_name=conf['section_name'], 
                item_key_field='SkillIdx', 
                item_key_value=skill_id, 
                field_name='Instant_Execute', 
                new_value=new_value
            )
        
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
        self._instant_cast_scps(skill_scp, mb_scp, pvp_scp, skill_id, new_value)
        new_dec = self._instant_cast_dec(skill_dec, skill_id, new_value)

        return new_dec