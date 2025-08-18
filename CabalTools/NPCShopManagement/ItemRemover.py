import copy

class ItemRemover:
    def __init__(self):
        pass

    def _set_proper_pool_id(self, pool_npc_map, pool_id_or_name):
        pool_id = None
        if isinstance(pool_id_or_name, int) and pool_id_or_name in pool_npc_map.keys():
            pool_id = pool_id_or_name

        if isinstance(pool_id_or_name, str):
            for pool, npc_name in pool_npc_map.items():
                if npc_name and pool_id_or_name in npc_name:
                    pool_id = pool

        if pool_id:
            return pool_id
        else:
            raise ValueError('ERROR: Unable to find a Pool_ID based on provided name.')
        
    def _is_item_in_shop(self, scp_data, Pool_ID, TabID, SlotID):
        shop_entries = [x['entries'] for x in scp_data if x['section'] == 'Shop'][0]
        for shop_item in shop_entries:
            if shop_item['Pool_ID'] == Pool_ID and shop_item['TabID'] == TabID and shop_item['SlotID'] == SlotID:
                return True
        return False

    def _filter_shop_entries(self, entries, Pool_ID, TabID, SlotID):
        new_entries = [
            e for e in entries
            if not (e['Pool_ID'] == Pool_ID and e['TabID'] == TabID and e['SlotID'] == SlotID)
        ]
        if new_entries:
            start_index = min(e['RowIndex'] for e in new_entries)
        else:
            start_index = 0
        for i, entry in enumerate(new_entries, start=start_index):
            entry['RowIndex'] = i
        return new_entries
    
    def remove_item_from_shop(self, scp_data, pool_npc_map, pool_id_or_name, TabID, SlotID):
        Pool_ID = self._set_proper_pool_id(pool_npc_map, pool_id_or_name)
        if not self._is_item_in_shop(scp_data, Pool_ID, TabID, SlotID):
            print('WARN: There is no such item in the NPC shop. Skipping ...')
            return data_copy
        
        data_copy = copy.deepcopy(scp_data)

        shop_section = next((s for s in data_copy if s['section'] == 'Shop'), None)
        if not shop_section:
            raise ValueError("ERROR: No 'Shop' section found in data.")
        
        shop_section['entries'] = self._filter_shop_entries(
            shop_section['entries'], 
            Pool_ID, 
            TabID, 
            SlotID
        )

        return data_copy
    

    