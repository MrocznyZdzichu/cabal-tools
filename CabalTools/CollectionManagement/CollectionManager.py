import copy

from ..FileHandling.SCPData    import SCPData
from ..FileHandling.SCPPreview import SCPPreview
from ..FileHandling.XMLSaver   import XMLSaver

from .ConfigPreprocessor import ConfigPreprocessor
from .MissionRemover     import MissionRemover
from .MissionAdder       import MissionAdder
from .RewardChanger      import RewardChanger


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

    def delete_mission(self, c_type, c_id, m_id, do_reinit=False, save_files=True, rebuild_indexes=False):
        MissionRemover().delete_mission(
        self._scp_data,
        self._dec_data,
        self._colle_tab_map,
        self._mission_tab_map,
        c_type, c_id, m_id
    )

        if rebuild_indexes:
            self.rebuild_scp_indexes()
        if save_files:
            self.save_files()
        if do_reinit:
            self.reinit()

    def add_mission(self, c_type, c_id, reward_type, reward_id, c_reward_id, slots_config, do_reinit=False, save_files=True, rebuild_indexes=False):
        MissionAdder.add_mission(self._scp_data, self._dec_data, c_type, c_id, reward_type, reward_id, c_reward_id, slots_config)

        if rebuild_indexes:
            self.rebuild_scp_indexes()
        if save_files:
            self.save_files()
        if do_reinit:
            self.reinit()

    def change_reward(self, c_reward_id, reward_ability, value_type, values, rebuild_indexes=False, save_files=True, do_reinit=False):
        RewardChanger().change_collection_reward(self._scp_data, self._dec_data, c_reward_id ,reward_ability, value_type, values)

        if rebuild_indexes:
            self.rebuild_scp_indexes()
        if save_files:
            self.save_files()
        if do_reinit:
            self.reinit()