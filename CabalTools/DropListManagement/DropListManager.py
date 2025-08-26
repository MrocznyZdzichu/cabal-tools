import copy
from dataclasses import asdict

from ..ABCBaseManager          import ABCBaseManager, can_reconfig
from ..FileHandling.SCPPreview import SCPPreview
from ..FileHandling.SCPData    import SCPData


class DropListManager(ABCBaseManager):
    def __init__(self, scp_data:SCPData, mobs_msg, mobs_dict, world_msg, world_dict, items_msg, items_dict):
        self._mobs_msg   = mobs_msg
        self._mobs_dict  = mobs_dict

        self._world_msg  = world_msg
        self._world_dict = world_dict

        self._items_msg  = items_msg
        self._items_dict = items_dict

        self._join_mappings = {
            'world_names' : {'key' : 'WorldIdx',   'value_col_name' : 'WorldName',   'source_dict' : self._world_dict},
            'mob_names'   : {'key' : 'SpeciesIdx', 'value_col_name' : 'SpeciesName', 'source_dict' : self._mobs_dict},
            'item_names'  : {'key' : 'ItemKind',   'value_col_name' : 'ItemName',    'source_dict' : self._items_dict},
        }
        self._drop_types = {
            'Box'    : {'section_name' : 'World_BoxDrop'},
            'Mob'    : {'section_name' : 'World_MobsDrop'},
            'Common' : {'section_name' : 'World_CommDrop'}
        }
        self._scp_data   = scp_data
        self._box_map    = self._build_box_id_map()
        super().__init__(scp_data=scp_data, scp_target_filename='World_drop.scp')
        

    def _build_box_id_map(self):
        return {
            y['BoxIdx'] :  y['SpeciesIdx'] 
            for y in [x['entries'] 
                for x in self._scp_data.data
                if x['section'] == 'Box_Main'
            ][0]
        }

    def _enrich_scp(self):
        data_copy = copy.deepcopy(self._scp_data.data)

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

    def rebuild_scp_index(self, section_name):
        self._scp_data.rebuild_rowindex(section_name)

    def _set_section(self, drop_type):
        if drop_type not in self._drop_types.keys():
            print('Passes a wrong droplist type. Omitting ...')
            return None
        
        return self._drop_types[drop_type]['section_name']
    
    @can_reconfig
    def remove_drop_from_list(self, drop_type, drop_index, rebuild_index=False):
        section_name = self._set_section(drop_type)
        if not section_name:
            return
        
        self._scp_data.remove_entry(section_name, drop_index, rebuild_index)

    @can_reconfig
    def add_drop(self, drop_type, drop_item):
        section_name = self._set_section(drop_type)
        if not section_name:
            return
        entries = self._scp_data.get_section(section_name)
        new_row_index = max([entry['RowIndex'] for entry in entries]) + 1 if entries else 1
        
        entry = {'RowIndex' : new_row_index}
        entry.update(asdict(drop_item))
        
        self._scp_data.add_entry(section_name, entry)
