from collections import defaultdict

from ..FileHandling.SCPData import SCPData


class ConfigPreprocessor:
    def __init__(self, dec_data, scp_data:SCPData, forcecodes: dict):
        self._dec_data   = dec_data
        self._scp_data   = scp_data
        self._stats_dict = forcecodes

    def _build_reward_dict(self):
        rewards_dict = {}

        gem_rewards_dict = {
            str(1) + '--' + str(x['attributes']['reward_id']) : str(x['attributes']['zem_qty'])+' Force Gems'
                for x in self._dec_data['children'][6]['children']
            }
        item_rewards_dict = {
            str(2) + "--" + str(x["attributes"]["reward_id"]): {
                "ItemKind": x["attributes"]["item_kind"],
                "ItemOpt": x["attributes"]["item_opt"],
            }
            for x in self._dec_data["children"][7]["children"]
        }
        rewards_dict |= gem_rewards_dict
        rewards_dict |= item_rewards_dict

        return rewards_dict

    def _build_stat_string(self, entry):
        stat_name = self._stats_dict[int(entry['attributes']['reward_ability'])]
        separator = {'1' : '', '2' : '%'}[entry['attributes']['value_type']]
        stat_val1 = entry['attributes']['ability_value1']
        stat_val2 = entry['attributes']['ability_value2']
        stat_val3 = entry['attributes']['ability_value3']

        return f"{stat_name}: {stat_val1}{separator} / {stat_val2}{separator} / {stat_val3}{separator}"

    def _build_colle_reward_dict(self):
        return {
            x['attributes']['c_reward_id'] : self._build_stat_string(x)
                for x in self._dec_data['children'][8]['children']
        }
  
    def _build_mission_id_map(self):
        colle_tab_map   = {(x['c_type'], x['c_id'], x['mission_id']) : x['RowIndex'] for x in self._scp_data.get_section('Collection')}
        mission_tab_map = defaultdict(list)
        for row in self._scp_data.get_section('Mission'):
            key = (row["c_type"], row["c_id"], row["mission_id"])
            mission_tab_map[key].append(row["RowIndex"])
        
        return colle_tab_map, mission_tab_map