import copy

from ..ABCBaseManager               import ABCBaseManager
from ..FileHandling.SCPxMsgJoiner   import SCPxMsgJoiner
from ..FileHandling.SCPPreview      import SCPPreview
from ..FileHandling.SCPData         import SCPData

from .ItemAdder                     import ItemAdder
from .ItemRemover                   import ItemRemover


class NPCShopManager(ABCBaseManager):
    def __init__(self, scp_data: SCPData, msg_data, item_msg, items_msg_map: dict):
        self._item_msgs       = item_msg
        self._msg_map         = items_msg_map
        super().__init__(
            scp_data=scp_data, 
            msg_data=msg_data, 
            scp_target_filename='NPCShop.scp'
        )

        self._item_adder      = ItemAdder()
        self._item_remover    = ItemRemover()

    def _enrich_scp(self):
        self._enriched_data1  = self._enrich_npc_section()
        self._npc_pool_map    = self._build_npc_pool_map()
        return self._enrich_shop_section()

    def _enrich_npc_section(self):        
        enriched_scp = copy.deepcopy(self._scp_data.data)
        for section in enriched_scp:
            if section['section'] == 'NPC':
                for entry in section['entries']:
                    entry['WorldNPCIdx'] = 'npc' + '0'*(2-len(str(entry['World_ID']))) + str(entry['World_ID']) + '-' + '0'*(4-len(str(entry['NPC_ID']))) + str(entry['NPC_ID'])
    
        enriched_scp = SCPxMsgJoiner().join_scp_with_msg(
            scp           = enriched_scp, 
            msg           = self._msg_data, 
            scp_key       = 'WorldNPCIdx', 
            key_build_fun = lambda WorldNPCIdx: str(WorldNPCIdx), 
            msg_key       = 'id', 
            msg_val       = 'cont', 
            new_idx_name  = 'NPC_Name'
        )
        return enriched_scp

    def _build_npc_pool_map(self):
        NPC_names = {}
        for entry in [section['entries'] for section in self._enriched_data1 if section['section'] == 'NPC'][0]:
            NPC_names[entry['Pool_ID1']] = entry['NPC_Name']
        return NPC_names

    def _enrich_shop_section(self):
        if not self._enriched_data1:
            self._enrich_npc_section()

        new_scp = copy.deepcopy(self._enriched_data1)

        for section in new_scp:
            if section['section'] == 'Shop':
                for entry in section['entries']:
                    v = self._msg_map.get(entry['ItemKind'])
                    entry['Item_Name'] = v['cont'] if v else None
                    entry['NPC_Name'] = self._npc_pool_map[entry['Pool_ID']]
                    
            elif section['section'] == 'ItemPrice':
                for entry in section['entries']:
                    entry['Item_Name'] = self._msg_map.get(entry['Index'])

        return new_scp

    def preview_NPCs(self, columns_to_show=None, filter_key=None, filter_val=None, filter_operator=None):
        data = SCPPreview().preview(
            self._enriched_data1, 
            section_name    = 'NPC', 
            columns         = columns_to_show, 
            filter_key      = filter_key, 
            filter_val      = filter_val, 
            filter_operator = filter_operator
        )
        return data
        
    def preview_shops(self, section=None, columns_to_show=None, filter_key=None, filter_val=None, filter_operator=None):
        if not section:
            section = ['Shop', 'ItemPrice']

        data = SCPPreview().preview(
            self._enriched_data,
            section_name    = section, 
            columns         = columns_to_show, 
            filter_key      = filter_key, 
            filter_val      = filter_val, 
            filter_operator = filter_operator
        )
        return data
    
    def add_item_to_shop(self, pool_or_or_npc_name, shop_slot_id, shop_item_to_add, shop_tab_id=0, save_files=True, do_reinit=False):
        self._item_adder.add_item_to_shop( 
            npcshop_scp_data = self._scp_data, 
            pool_npc_map     = self._npc_pool_map, 
            pool_id_or_name  = pool_or_or_npc_name, 
            slot_id          = shop_slot_id,     
            shop_item        = shop_item_to_add,
            tab_id           = shop_tab_id
        )

        if save_files:
            self.save()

        if do_reinit:
            self.reinit()
    
    def batch_add_item_to_shop(self, pool_or_or_npc_name, slot_x_shopitem_dict: dict, shop_tab_id, save_files=True, do_reinit=False):
        for key, items in slot_x_shopitem_dict.items():
            self._item_adder.add_item_to_shop( 
                npcshop_scp_data = self._scp_data, 
                pool_npc_map     = self._npc_pool_map, 
                pool_id_or_name  = pool_or_or_npc_name, 
                slot_id          = key,     
                shop_item        = items,
                tab_id           = shop_tab_id
            )
        if save_files:
            self.save()

        if do_reinit:
            self.reinit()
            
    def remove_item_from_shop(self, pool_id_or_name, TabID, SlotID, save_files=True, do_reinit=False):
        self._item_remover.remove_item_from_shop(
            scp_data         = self._scp_data, 
            pool_npc_map     = self._npc_pool_map, 
            pool_id_or_name  = pool_id_or_name, 
            TabID            = TabID, 
            SlotID           = SlotID
        )
        if save_files:
            self.save()

        if do_reinit:
            self.reinit()
    
    def batch_remove_item_from_shop(self, removed_items_data, do_reinit=False, save_files=True):
        for key, items in removed_items_data.items():
            self._item_remover.remove_item_from_shop(
                scp_data         = self._scp_data, 
                pool_npc_map     = self._npc_pool_map, 
                pool_id_or_name  = items['pool_id_or_name'], 
                TabID            = items['TabID'], 
                SlotID           = items['SlotID']
            )

        if do_reinit:
            self.reinit()

        if save_files:
            self.save()