class SkillDataParser:
    def __init__(self):
        pass

    def get_skill_xml_name(self, skill_msgs_text, skill_name):
        return [x['id'] for x in skill_msgs_text if x['cont'] == skill_name][0]
    
    def get_skill_main_from_dec(self, skill_msgs_text, skill_dec_text, skill_name):
        new_skill_list_section = [x for x in skill_dec_text['children'] if x['tag'] == 'new_skill_list'][0]['children']
        name_in_xml = self.get_skill_xml_name(skill_msgs_text, skill_name)
        return [x for x in new_skill_list_section if 'name' in x['attributes'].keys() and x['attributes']['name'] == name_in_xml][0]
    
    def get_skill_id(self, skill_msgs_text, skill_dec_text, skill_name):
        skill_dec_data = self.get_skill_main_from_dec(skill_msgs_text, skill_dec_text, skill_name)
        return skill_dec_data['attributes']['id'] if 'id' in skill_dec_data['attributes'] else None
    
    def get_skill_main_from_scp(self, skill_scp_data, skill_id):
        Skill_main_entries = [x['entries'] for x in skill_scp_data if x['section'] == 'SKill_Main'][0]
        return [x for x in Skill_main_entries if x['SkillIdx'] == skill_id][0]