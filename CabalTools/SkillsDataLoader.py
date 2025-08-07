import re
from .XMLSectionLoader import XMLSectionLoader
from .XMLAttributesParser import XMLAttributesParser
from .SCPLoader import SCPLoader

class SkillsDataLoader:
    def __init__(self, skill_dec_path, cabal_msg_path, skill_scp_path, skill_mb_path=None, skill_pvp_path=None):
        self._skill_dec_path        = skill_dec_path
        self._cabal_msg_path        = cabal_msg_path
        self._msg_section_start     = '<cabal_msg>'
        self._msg_section_end       = '</cabal_msg>'
        self._skill_section_start   = '<cabal_skill>'
        self._skill_section_end     = '</cabal_skill>'
        self._skill_scp_path        = skill_scp_path

        if skill_mb_path is not None and skill_pvp_path is not None:
            self._skill_mb_path = skill_mb_path
            self._skill_pvp_path = skill_pvp_path    

        self._xml_loader = XMLSectionLoader()
        self._xml_parser = XMLAttributesParser()
        self._scp_loader = SCPLoader() 

    def _msg_skills_only(self, cabal_messages_dict):
        return [x['attributes'] for x in cabal_messages_dict['children'] if re.search(r'skill\d+', x['attributes'].get('id', ''))]
    
    def load(self):
        cabal_messages = self._xml_loader.load_xml_section(self._cabal_msg_path, self._msg_section_start, self._msg_section_end)
        cabal_messages_dict = self._xml_parser.xml_string_to_dict(cabal_messages)
        cabal_skill_names   = self._msg_skills_only(cabal_messages_dict)

        skill_details = self._xml_loader.load_xml_section(self._skill_dec_path, self._skill_section_start, self._skill_section_end)
        skill_details_dict = self._xml_parser.xml_string_to_dict(skill_details)

        skill_scp_data = self._scp_loader.load_scp_file(self._skill_scp_path)
        
        if self._skill_mb_path is not None and self._skill_pvp_path is not None:
            skill_mb_data = self._scp_loader.load_scp_file(self._skill_mb_path)
            skill_pvp_data = self._scp_loader.load_scp_file(self._skill_pvp_path)
            return cabal_skill_names, skill_details_dict, skill_scp_data, skill_mb_data, skill_pvp_data
        
        return cabal_skill_names, skill_details_dict, skill_scp_data