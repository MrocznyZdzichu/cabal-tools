import copy

from ..FileHandling.SCPxMsgJoiner   import SCPxMsgJoiner
from ..FileHandling.SCPPreview      import SCPPreview


class NPCShopManager:
    def __init__(self, npc_shops_scp_data, npc_related_messages, items_related_messages):
        self._npc_scp         = npc_shops_scp_data
        self._npc_msg         = npc_related_messages
        self._item_msgs       = items_related_messages
        self._enriched_data1  = self._enrich_npc_section()
        self._enriched_data2  = self._enrich_shop_section()

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

    def _enrich_shop_section(self):
        if not self._enriched_data1:
            self._enrich_npc_section()

        new_scp = copy.deepcopy(self._enriched_data1)
        new_msg = copy.deepcopy(self._item_msgs)

        NPC_names = {}
        for entry in [section['entries'] for section in new_scp if section['section'] == 'NPC'][0]:
            NPC_names[entry['Pool_ID1']] = entry['NPC_Name']

        for section in new_scp:
            if section['section'] == 'Shop':
                for entry in section['entries']:
                    item_name = [x['cont'] for x in new_msg if x['ItemKind'] == entry['ItemKind']]
                    entry['Item_Name'] = item_name[0] if len(item_name) > 0 else None
                    entry['NPC_Name'] = NPC_names[entry['Pool_ID']]
                    
            if section['section'] == 'ItemPrice':
                for entry in section['entries']:
                    item_name = [x['cont'] for x in new_msg if x['ItemKind'] == entry['Index']]
                    entry['Item_Name'] = item_name[0] if len(item_name) > 0 else None

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

        SCPPreview().preview(
            self._enriched_data2,
            section_name    = section, 
            columns         = columns_to_show, 
            filter_key      = filter_key, 
            filter_val      = filter_val, 
            filter_operator = filter_operator
        )