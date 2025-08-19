import re
from abc import ABC, abstractmethod

from ..FileHandling.SCPLoader           import SCPLoader
from ..FileHandling.XMLSectionLoader    import XMLSectionLoader
from ..FileHandling.XMLAttributesParser import XMLAttributesParser


class ABCSpecificLoader(ABC):
    def __init__(
            self, 
            scp_path=None, 
            dec_path=None, 
            messages_path=None, 
            dec_section_start=None, 
            dec_section_end=None, 
            msg_section_start=None, 
            msg_section_end=None
        ):
        self._scp_path = scp_path
        self._dec_path = dec_path
        self._msg_path = messages_path

        self._dec_section_start = dec_section_start
        self._dec_section_end   = dec_section_end
        self._msg_section_start = msg_section_start
        self._msg_section_end   = msg_section_end

        self._scp_loader = SCPLoader()
        self._xml_loader = XMLSectionLoader()
        self._xml_parser = XMLAttributesParser()

    def _load_scp_file(self):
        return self._scp_loader.load_scp_file(self._scp_path)
    
    def _load_msgs(self):
        cabal_messages = self._xml_loader.load_xml_section(
            self._msg_path, self._msg_section_start, self._msg_section_end
        )
        return self._xml_parser.xml_string_to_dict(cabal_messages)

    def _load_dec(self):
        dec_data = self._xml_loader.load_xml_section(
            self._dec_path, self._dec_section_start, self._dec_section_end
        )
        return self._xml_parser.xml_string_to_dict(dec_data)
    
    def _pick_msgs_section(self, cabal_messages_dict, regex_filter):
        return [
            x['attributes']
            for x in cabal_messages_dict['children']
            if re.search(regex_filter, x['attributes'].get('id', ''))
        ]

    @abstractmethod
    def load(self):
        pass
