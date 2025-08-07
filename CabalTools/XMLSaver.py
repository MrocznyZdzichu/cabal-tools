import xml.etree.ElementTree as ET

class XMLSaver:
    def __init__(self):
        pass

    def _dict_to_element(self, data):
        elem = ET.Element(data['tag'], attrib=data.get('attributes', {}))
        if 'text' in data and data['text']:
            elem.text = data['text']
        for child in data.get('children', []):
            elem.append(self._dict_to_element(child))
        return elem

    def _format_attributes(self, attrib):
        if not attrib:
            return ""
        return ''.join(f'\t{key}="{value}"' for key, value in attrib.items())

    def _element_to_string(self, elem, level=0):
        indent = '\t' * level
        tag = elem.tag
        attrs = self._format_attributes(elem.attrib)

        children = list(elem)
        if not children:
            if attrs:
                return f'{indent}<{tag}{attrs}\t/>'
            else:
                return f'{indent}<{tag}/>'
        else:
            if attrs:
                open_tag = f'{indent}<{tag}{attrs}\t>'
            else:
                open_tag = f'{indent}<{tag}>'
            lines = [open_tag]
            for child in children:
                lines.append(self._element_to_string(child, level + 1))
            lines.append(f'{indent}</{tag}>')
            return '\n'.join(lines)

    def dict_to_xml_string(self, data):
        elem = self._dict_to_element(data)
        body = self._element_to_string(elem)
        return '\n' + body 

    def save_dict_to_file(self, data, filepath):
        xml_str = self.dict_to_xml_string(data)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(xml_str)
