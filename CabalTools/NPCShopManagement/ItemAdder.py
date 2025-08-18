import copy
from dataclasses import asdict

from .ShopItem import ShopItem

class ItemAdder:
    def __init__(self):
        pass

    def _set_proper_pool_id(self, pool_npc_map, pool_id_or_name):
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
        
    def _check_is_slot_occupied(
        self,
        npcshop_scp_data,
        pool_id,
        slot_id,
        tab_id=0,
    ):
        shop_entries = [x['entries'] for x in npcshop_scp_data if x['section'] == 'Shop'][0]
        slots_occupied = [entry['SlotID'] for entry in shop_entries 
                        if entry['Pool_ID'] == pool_id and entry['TabID'] == tab_id]

        return slot_id in slots_occupied

    def _create_shop_entry(
        self,
        new_row_index: int,
        pool_id: int,
        tab_id: int,
        slot_id: int,
        shop_item: ShopItem
    ):
        entry = {
            "RowIndex": new_row_index,
            "Pool_ID": pool_id,
            "TabID": tab_id,
            "SlotID": slot_id
        }
        entry.update(asdict(shop_item))
        return entry

    def add_item_to_shop(
        self, 
        npcshop_scp_data, 
        pool_npc_map, 
        pool_id_or_name, 
        slot_id,     
        shop_item: ShopItem,
        tab_id=0
    ):
        data_copy = copy.deepcopy(npcshop_scp_data)
        pool_id = self._set_proper_pool_id(pool_npc_map, pool_id_or_name)

        if self._check_is_slot_occupied(npcshop_scp_data, pool_id, slot_id, tab_id):
            print('WARN: The slot is already occupied by an other item. Omitting ...')
            return data_copy
        
        shop_section = next((x for x in data_copy if x['section'] == 'Shop'), None)
        if shop_section is None:
            raise ValueError("ERROR: No 'Shop' section found in data!")

        shop_entries = shop_section['entries']
        new_row_index = max([entry['RowIndex'] for entry in shop_entries]) + 1 if shop_entries else 1

        new_entry = self._create_shop_entry(
            new_row_index,
            pool_id,
            tab_id,
            slot_id,
            shop_item
        )

        shop_entries.append(new_entry)
        return data_copy