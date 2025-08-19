import copy

from ..FileHandling import SCPPreview
from ..FileHandling import SCPxMsgJoiner


class DropListManager:
    def __init__(self, scp_data, mobs_msg, mobs_dict, world_msg, world_dict, items_msg, items_dict):
        self._scp_data   = scp_data

        self._mobs_msg   = mobs_msg
        self._mobs_dict  = mobs_dict
        self._box_map    = self._build_box_id_map()
        
        self._world_msg  = world_msg
        self._world_dict = world_dict

        self._items_msg  = items_msg
        self._items_dict = items_dict
        
        self._join_mappings = {
            'world_names' : {'key' : 'WorldIdx', 'value_col_name' : 'WorldName', 'source_dict' : self._world_dict},
            'mob_names'   : {'key' : 'SpeciesIdx', 'value_col_name' : 'SpeciesName', 'source_dict' : self._mobs_dict},
            'item_names'  : {'key' : 'ItemKind', 'value_col_name' : 'ItemName', 'source_dict' : self._items_dict},
        }
        self._scp_with_names = self._join_names()

    def _build_box_id_map(self):
        return {
            y['BoxIdx'] :  y['SpeciesIdx'] 
            for y in [x['entries'] 
                for x in self._scp_data 
                if x['section'] == 'Box_Main'
            ][0]
        }
    
    def _join_names(self):
        data_copy = copy.deepcopy(self._scp_data)

        for section in data_copy:    
            for entry in section.get("entries", []):
                if section['section'] == 'World_BoxDrop':
                    entry['SpeciesIdx'] = self._box_map[entry['BoxIdx']]
                for k, v in self._join_mappings.items():
                    if v['key'] in entry:
                        key = entry[v['key']]
                        value = v['source_dict'].get(key)
                        entry[v['value_col_name']] = value["cont"] if value else None

        return data_copy
            
    def preview_drop_lists(self, section=None, columns = None, filter_key = None, filter_val = None, filter_operator = None):
        return SCPPreview().preview(
            self._scp_with_names,
            section_name    = section, 
            columns         = columns, 
            filter_key      = filter_key, 
            filter_val      = filter_val, 
            filter_operator = filter_operator
        )
