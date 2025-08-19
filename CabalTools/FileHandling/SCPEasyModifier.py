import copy


class SCPEasyModifier:
    def __init__(self):
        pass

    def modify_scp_row(self, scp_data, section_name, item_key_field, item_key_value, field_name, new_value):
        updated_dict = copy.deepcopy(scp_data)
        for section in updated_dict:
            if section['section'] == section_name:
                for item in section['entries']:
                    if str(item[item_key_field]) == str(item_key_value):
                        item[field_name] = new_value
                        
        return updated_dict