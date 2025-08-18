import xml.etree.ElementTree as ET
import re

class XMLAttributesParser:
    def __init__(self):
        pass

    def _escape_xml_entities(self, xml_string):
        return re.sub(r'&(?!amp;|lt;|gt;|apos;|quot;)', '&amp;', xml_string)

    def _element_to_dict(self, elem):
        node = {
            'tag': elem.tag,
            'attributes': elem.attrib,
            'text': elem.text.strip() if elem.text and elem.text.strip() else None,
            'children': [self._element_to_dict(child) for child in elem]
        }
        return {k: v for k, v in node.items() if v} 

    def xml_string_to_dict(self, xml_string):
        xml_string = self._escape_xml_entities(xml_string)
        root = ET.fromstring(xml_string)
        return self._element_to_dict(root)

    def _dict_to_element(self, data):
        elem = ET.Element(data['tag'], attrib=data.get('attributes', {}))
        if 'text' in data:
            elem.text = data['text']
        for child_data in data.get('children', []):
            elem.append(self._dict_to_element(child_data))
        return elem

    def dict_to_xml_string(self, data):
        root_elem = self._dict_to_element(data)
        return ET.tostring(root_elem, encoding='unicode')
