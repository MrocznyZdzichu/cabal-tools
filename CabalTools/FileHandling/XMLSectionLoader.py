class XMLSectionLoader:
    def __init__(self):
        pass

    def load_xml_section(self, filepath, section_start, section_end):
        section_lines = []
        inside_section = False

        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                if section_start in line:
                    inside_section = True
                if inside_section:
                    section_lines.append(line)
                if section_end in line and inside_section:
                    break

        return ''.join(section_lines)
