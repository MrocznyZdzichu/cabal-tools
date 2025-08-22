from ..FileHandling.SCPData import SCPData


class RewardChanger:
    @staticmethod
    def _scp_change_reward(scp_data: SCPData, c_reward_id ,reward_ability, value_type, values: tuple):
        scp_data.modify_field(
            section_name='Collection_reward', 
            item_key_field='c_reward_id', 
            item_key_value=c_reward_id, 
            field_name='reward_ability', 
            new_value=reward_ability
        )
        scp_data.modify_field(
            section_name='Collection_reward', 
            item_key_field='c_reward_id', 
            item_key_value=c_reward_id, 
            field_name='value_type', 
            new_value=value_type
        )
        for it, val in enumerate(values):
            col_key = f'ability_value{it+1}'
            scp_data.modify_field(
                section_name='Collection_reward', 
                item_key_field='c_reward_id', 
                item_key_value=c_reward_id, 
                field_name=col_key, 
                new_value=val
            )

    @staticmethod
    def _dec_change_reward(dec_data: dict, c_reward_id ,reward_ability, value_type, values: tuple):
        c_reward_id    = str(c_reward_id)
        reward_ability = str(reward_ability)
        value_type     = str(value_type)
        
        for val in values:
            val = str(val)

        for entry in dec_data['children'][8]['children']:
            ea = entry['attributes']
            if ea['c_reward_id'] == c_reward_id:
                ea['reward_ability'] = reward_ability
                ea['value_type'] = value_type
                for it, val in enumerate(values):
                    col_key = f'ability_value{it+1}'
                    ea[col_key] = val

    @staticmethod
    def change_collection_reward(scp_data: SCPData, dec_data, c_reward_id ,reward_ability, value_type, values: tuple):
        RewardChanger._scp_change_reward(scp_data, c_reward_id ,reward_ability, value_type, values)
        RewardChanger._dec_change_reward(dec_data, c_reward_id ,reward_ability, value_type, values)