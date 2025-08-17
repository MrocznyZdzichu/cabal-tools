import copy

from ..FileHandling.SCPxMsgJoiner   import SCPxMsgJoiner
from ..FileHandling.SCPPreview      import SCPPreview
from ..FileHandling.SCPSaver        import SCPSaver
from .ItemAdder                     import ItemAdder
from .ItemRemover                   import ItemRemover


class NPCShopManager:
    def __init__(self, npc_shops_scp_data, npc_related_messages, items_related_messages):
        self._npc_scp         = npc_shops_scp_data
        self._npc_msg         = npc_related_messages
        self._item_msgs       = items_related_messages
        self._enriched_data1  = self._enrich_npc_section()
        self._npc_pool_map    = self._build_npc_pool_map()
        self._enriched_data2  = self._enrich_shop_section()

        self._item_adder      = ItemAdder()
        self._item_remover    = ItemRemover()

        self._target_scp_name = 'NPCShop.scp'

    def _enrich_npc_section(self):        
        enriched_scp = copy.deepcopy(self._npc_scp)
        for section in enriched_scp:
            if section['section'] == 'NPC':
                for entry in section['entries']:
                    entry['WorldNPCIdx'] = 'npc' + '0'*(2-len(str(entry['World_ID']))) + str(entry['World_ID']) + '-' + '0'*(4-len(str(entry['NPC_ID']))) + str(entry['NPC_ID'])
    
        enriched_scp = SCPxMsgJoiner().join_scp_with_msg(
            scp           = enriched_scp, 
            msg           = self._npc_msg, 
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
        new_msg = copy.deepcopy(self._item_msgs)
        
        msg_map = {x['ItemKind']: x['cont'] for x in new_msg}

        for section in new_scp:
            if section['section'] == 'Shop':
                for entry in section['entries']:
                    entry['Item_Name'] = msg_map.get(entry['ItemKind'])
                    entry['NPC_Name'] = self._npc_pool_map[entry['Pool_ID']]
                    
            elif section['section'] == 'ItemPrice':
                for entry in section['entries']:
                    entry['Item_Name'] = msg_map.get(entry['Index'])

        return new_scp

    def reinit(self, new_shop_scp_data):
        self._npc_scp         = new_shop_scp_data
        self._enriched_data1  = self._enrich_npc_section()
        self._enriched_data2  = self._enrich_shop_section()

    def preview_NPCs(self, columns_to_show=None, filter_key=None, filter_val=None, filter_operator=None):
        SCPPreview().preview(
            self._enriched_data1, 
            section_name    = 'NPC', 
            columns         = columns_to_show, 
            filter_key      = filter_key, 
            filter_val      = filter_val, 
            filter_operator = filter_operator)
        
    def preview_shops(self, section=None, columns_to_show=None, filter_key=None, filter_val=None, filter_operator=None):
        if not section:
            section = ['Shop', 'ItemPrice']

        data = SCPPreview().preview(
            self._enriched_data2,
            section_name    = section, 
            columns         = columns_to_show, 
            filter_key      = filter_key, 
            filter_val      = filter_val, 
            filter_operator = filter_operator
        )
        return data
    
    def add_item_to_shop(self, pool_or_or_npc_name, shop_slot_id, shop_item_to_add, shop_tab_id=0, save_files=True, do_reinit=False):
        new_shop_scp = self._item_adder.add_item_to_shop( 
            npcshop_scp_data = self._npc_scp, 
            pool_npc_map     = self._npc_pool_map, 
            pool_id_or_name  = pool_or_or_npc_name, 
            slot_id          = shop_slot_id,     
            shop_item        = shop_item_to_add,
            tab_id           = shop_tab_id
        )

        if save_files:
            scp_saver = SCPSaver()
            scp_saver.save_scp_file(new_shop_scp, self._target_scp_name)

        if do_reinit:
            self.reinit(new_shop_scp)
            
        return new_shop_scp
    
    def remove_item_from_shop(self, pool_id_or_name, TabID, SlotID, save_files=True, do_reinit=False):
        new_shop_scp = self._item_remover.remove_item_from_shop(
            scp_data         = self._npc_scp, 
            pool_npc_map     = self._npc_pool_map, 
            pool_id_or_name  = pool_id_or_name, 
            TabID            = TabID, 
            SlotID           = SlotID
        )
        if save_files:
            scp_saver = SCPSaver()
            scp_saver.save_scp_file(new_shop_scp, self._target_scp_name)

        if do_reinit:
            self.reinit(new_shop_scp)
            
        return new_shop_scp