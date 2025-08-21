import copy

from ..FileHandling.SCPData    import SCPData
from ..FileHandling.SCPPreview import SCPPreview
from ..FileHandling.XMLSaver   import XMLSaver

from .ConfigPreprocessor import ConfigPreprocessor


class CollectionManager:

    def __init__(
        self,
        # Data from the main loader
        scp_data: SCPData,
        dec_data: dict,
        msg_data: dict,
        c_types_dict: dict,
        c_id_dict: dict,
        m_id_dict: dict,
        r_type_dict: dict,
        item_type: dict,
        item_name: dict,
        # Data from bonus item loader
        item_rel_msgs: dict, 
        item_msg_dict: dict,
    ):
        self._scp_data     = scp_data
        self._dec_data     = dec_data
        self._msg_data     = msg_data
        self._c_types_dict = c_types_dict
        self._c_id_dict    = c_id_dict
        self._m_id_dict    = m_id_dict
        self._r_types_dict = r_type_dict
        self._item_type    = item_type
        self._item_name    = item_name

        self._item_msg     = item_rel_msgs
        self._item_dict    = item_msg_dict
        
        self.reinit()

    def _get_exact_mission_reward(self, entry):
        if entry['m_reward_type'] == 1:
            return self._rew_dict.get(str(entry['m_reward_type']) + '--' + str(entry['m_reward_id']))
        elif entry['m_reward_type'] == 2:
            item_kind = int(self._rew_dict.get(str(entry['m_reward_type']) + '--' + str(entry['m_reward_id'])).get('ItemKind'))
            item_opt  = self._rew_dict.get(str(entry['m_reward_type']) + '--' + str(entry['m_reward_id'])).get('ItemOpt')
            item_name = self._item_dict.get(item_kind).get('cont')
            return  item_name + ' with option: ' + item_opt
    
    def _enrich_scp(self):
        rich_scp = copy.deepcopy(self._scp_data.data)

        for section in rich_scp:
            for entry in section['entries']:
                if section['section'] == 'Collection':
                    entry['ColleType']     = self._c_types_dict.get(entry['c_type'])
                    entry['ColleName']     = self._c_id_dict.get(str(entry['c_type']) + '--' + str(entry['c_id']))
                    entry['MissionName']   = self._m_id_dict.get(str(entry['c_type']) + '--' + str(entry['c_id']) + '--' + str(entry['mission_id']))
                    entry['MissionReward'] = self._get_exact_mission_reward(entry)
                    entry['ColleReward']   = self._colle_rew.get(str(entry['c_reward_id']))
                if section['section'] == 'Mission':
                    entry['ColleName']     = self._c_id_dict.get(str(entry['c_type']) + '--' + str(entry['c_id']))
                    entry['MissionName']   = self._m_id_dict.get(str(entry['c_type']) + '--' + str(entry['c_id']) + '--' + str(entry['mission_id']))
                    entry['ItemType']      = self._item_type.get(entry['m_item_type'])
                    entry['ItemName']      = self._item_name.get((str(entry['m_item_type']), str(entry['m_item_id'])))
                
        return rich_scp

    def reinit(self):
        self._config_analyser = ConfigPreprocessor(self._dec_data, self._scp_data)
        self._stats_dict = self._config_analyser._get_force_code_dict()
        self._rew_dict   = self._config_analyser._build_reward_dict()
        self._colle_rew  = self._config_analyser._build_colle_reward_dict()
        
        self._colle_tab_map, self._mission_tab_map = self._config_analyser._build_mission_id_map()
        
        self._rich_scp = self._enrich_scp()

    def save_files(self):
        self._scp_data.save_to_file('Collection.scp')
        XMLSaver().save_dict_to_file(self._dec_data, 'Collection.dec')

    def rebuild_scp_indexes(self):
        self._scp_data.rebuild_rowindex('Collection')
        self._scp_data.rebuild_rowindex('Mission')

    def preview_collection_data(
            self,
            section_name=['Collection', 'Mission'],
            columns=None,
            filter_key=None,
            filter_val=None,
            filter_operator=None,                    
        ):
        SCPPreview().preview(
            self._rich_scp,
            section_name=section_name,
            columns=columns,
            filter_key=filter_key,
            filter_val=filter_val,
            filter_operator=filter_operator,
        )

    def _delete_mission_scp(self, c_type, c_id, m_id):
        collection_entry_id = self._colle_tab_map.get((c_type, c_id, m_id))
        mission_entry_ids   = self._mission_tab_map.get((c_type, c_id, m_id))

        self._scp_data.remove_entry('Collection', collection_entry_id)
        for id in mission_entry_ids:
            self._scp_data.remove_entry('Mission', id)

        for section in ('Collection', 'Mission'):
            table = self._scp_data.get_section(section)
            for entry in table:
                if entry['c_type'] == c_type and entry['c_id'] == c_id and entry['mission_id'] > m_id:
                    entry['mission_id'] -= 1

    def _delete_mission_dec(self, c_type, c_id, m_id):
        c_type = str(c_type)
        c_id   = str(c_id)
        m_id   = str(m_id)

        for entry in self._dec_data['children'][2]['children']: # Collection_mission section
            ct = entry['attributes']['c_type']
            entry['children'] = [
                entry2 for entry2 in entry['children']
                if not (ct == c_type 
                        and entry2['attributes']['c_id'] == c_id 
                        and entry2['attributes']['mission_id'] == m_id)
            ]
            for entry2 in entry['children']:
                if ct == c_type and entry2['attributes']['c_id'] == c_id and int(entry2['attributes']['mission_id']) > int(m_id):
                    entry2['attributes']['mission_id'] = str(int(entry2['attributes']['mission_id']) - 1)

        for entry in self._dec_data['children'][1]['children']: # Collection_type section
            ct = entry['attributes']['type']
            if ct == c_type:
                for entry2 in entry['children']:
                    cd = entry2['attributes']['c_id']
                    if cd == c_id:
                        entry2['children'] = [
                            x for x in entry2['children'] 
                            if not (x['attributes']['mission_id'] == m_id)
                        ]
                        for entry3 in entry2['children']:
                            if int(entry3['attributes']['mission_id']) > int(m_id):
                                entry3['attributes']['mission_id'] = str(int(entry3['attributes']['mission_id']) - 1)


    def delete_mission(self, c_type, c_id, m_id, do_reinit=False, save_files=True, rebuild_indexes=False):
        self._delete_mission_scp(c_type, c_id, m_id)
        self._delete_mission_dec(c_type, c_id, m_id)

        if rebuild_indexes:
            self.rebuild_scp_indexes()
        if save_files:
            self.save_files()
        if do_reinit:
            self.reinit()