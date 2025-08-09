import copy

from ..FileHandling.SCPxMsgJoiner   import SCPxMsgJoiner


class NPCShopManager:
    def __init__(self, npc_shops_scp_data, npc_related_messages):
        self._npc_scp = npc_shops_scp_data
        self._npc_msg = npc_related_messages
        self._rich_npc_data = self._enrich_npc_scp()

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
        pass

    def _enrich_npc_scp(self):
        enriched = self._enrich_npc_section()
        # self._enrich_shop_section()
        return enriched

    def preview_NPCs(self):
        pass