class SCPData:
    def __init__(self, data):
        self.data = data if data is not None else []

    def list_sections(self):
        return [section["section"] for section in self.data]

    def get_section(self, section_name):
        for section in self.data:
            if section["section"] == section_name:
                return section["entries"]
        return None

    def add_entry(self, section_name, entry, rebuild_index=False):
        section = self.get_section(section_name)
        if section is not None:
            section.append(entry)
            if rebuild_index:
                self.rebuild_rowindex(section_name)
            return True
        return False

    def remove_entry(self, section_name, row_index_value, rebuild_index=False):
        section = self.get_section(section_name)
        if section is not None:
            for i, entry in enumerate(section):
                if entry.get("RowIndex") == row_index_value:
                    del section[i]
                    if rebuild_index:
                        self.rebuild_rowindex(section_name)
                    return True
        return False

    def update_entry(self, section_name, row_index_value, new_entry, rebuild_index=False):
        section = self.get_section(section_name)
        if section is not None:
            for i, entry in enumerate(section):
                if entry.get("RowIndex") == row_index_value:
                    section[i] = new_entry
                    if rebuild_index:
                        self.rebuild_rowindex(section_name)
                    return True
        return False

    def modify_field(self, section_name, item_key_field, item_key_value, field_name, new_value):
        for section in self.data:
            if section['section'] == section_name:
                for item in section['entries']:
                    if str(item[item_key_field]) == str(item_key_value):
                        item[field_name] = new_value
                        return True    
        return False
    
    def get_short_preview(self, n_entries=5):
        preview = []
        for section in self.data:
            preview.append({
                "section": section["section"],
                "entries": section["entries"][:n_entries]
            })
        return preview

    def save_to_file(self, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:            
            for section in self.data:
                f.write('\n\n')
                section_name = section['section']
                entries = section['entries']

                if not entries:
                    continue

                headers = [k for k in entries[0].keys() if k != "RowIndex"]

                f.write(f"[{section_name}]\t" + '\t'.join(headers) + '\n')

                for entry in entries:
                    row = [str(entry["RowIndex"])]
                    for key in headers:
                        val = entry.get(key, '')
                        if val is None:
                            val = "<null>"
                        row.append(str(val))
                    f.write('\t'.join(row) + '\n')

    def rebuild_rowindex(self, section_name, start=0):
        section = self.get_section(section_name)
        if section is not None:
            for offset, entry in enumerate(section):
                entry["RowIndex"] = start + offset
            return True
        return False



# class SCPData:
#     def __init__(self, data):
#         self.data = data if data is not None else []

#     def list_sections(self):
#         return [section["section"] for section in self.data]

#     def get_section(self, section_name):
#         for section in self.data:
#             if section["section"] == section_name:
#                 return section["entries"]
#         return None

#     def add_entry(self, section_name, entry):
#         section = self.get_section(section_name)
#         if section is not None:
#             section.append(entry)
#             return True
#         return False

#     def remove_entry(self, section_name, index):
#         section = self.get_section(section_name)
#         if section is not None and 0 <= index < len(section):
#             del section[index]
#             return True
#         return False

#     def update_entry(self, section_name, index, new_entry):
#         section = self.get_section(section_name)
#         if section is not None and 0 <= index < len(section):
#             section[index] = new_entry
#             return True
#         return False

#     def modify_field(self, section_name, item_key_field, item_key_value, field_name, new_value):
#         for section in self.data:
#             if section['section'] == section_name:
#                 for item in section['entries']:
#                     if str(item[item_key_field]) == str(item_key_value):
#                         item[field_name] = new_value
#                         return True    
#         return False
    
#     def get_short_preview(self, n_entries=5):
#         preview = []
#         for section in self.data:
#             preview.append({
#                 "section": section["section"],
#                 "entries": section["entries"][:n_entries]
#             })
#         return preview

#     def save_to_file(self, output_path):
#         with open(output_path, 'w', encoding='utf-8') as f:            
#             for section in self.data:
#                 f.write('\n\n')
#                 section_name = section['section']
#                 entries = section['entries']

#                 if not entries:
#                     continue

#                 headers = [k for k in entries[0].keys() if k != "RowIndex"]

#                 f.write(f"[{section_name}]\t" + '\t'.join(headers) + '\n')

#                 for entry in entries:
#                     row = [str(entry["RowIndex"])]
#                     for key in headers:
#                         val = entry.get(key, '')
#                         if val is None:
#                             val = "<null>"
#                         row.append(str(val))
#                     f.write('\t'.join(row) + '\n')
