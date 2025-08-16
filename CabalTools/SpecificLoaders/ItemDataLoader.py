from .ABCSpecificLoader   import ABCSpecificLoader
import copy

class ItemDataLoader(ABCSpecificLoader):
    def __init__(self, scp_path, messages_path):
        super().__init__(
            scp_path, 
            messages_path, 
            '<item_msg>', 
            '</item_msg>'
        )
        # self._upgrade_range      = list(range(0, 21))
        # self._upgrade_multiplier = 8192
        self._bound_codes        = {
            # 0       : '',
            4096    : 'Account Bound',
            524288  : 'Character Bound',
            1572864 : 'Char. Bound on Equip'
        }

    def _add_itemKind(self, loaded_item_messages):
        for entry in loaded_item_messages:
            entry["ItemKind"] = int(entry["id"].replace("item", ""))
        return loaded_item_messages
    
    def _expand_item_ids(self, loaded_item_messages):
        expanded_item_messages = loaded_item_messages

        acc_bound_items = copy.deepcopy(loaded_item_messages)
        for message in acc_bound_items:
            message['ItemKind'] += 4096
            message['cont'] += ' (Account Bound)'
            message['id'] = f'item{message['ItemKind']}'
        expanded_item_messages += acc_bound_items

        char_bound_items = copy.deepcopy(loaded_item_messages)
        for message in char_bound_items:
            message['ItemKind'] += 524288
            message['cont'] += ' (Character Bound)'
            message['id'] = f'item{message['ItemKind']}'
        expanded_item_messages += char_bound_items

        on_equip_bound_items = copy.deepcopy(loaded_item_messages)
        for message in on_equip_bound_items:
            message['ItemKind'] += 1572864
            message['cont'] += ' (Character Bound on Equip)'
            message['id'] = f'item{message['ItemKind']}'
        expanded_item_messages += char_bound_items

        return expanded_item_messages

    def load(self):
        # scp_data = self._load_scp_file() Item.scp is useless for me so far so it is kept as a mock
        cabal_messages = self._load_msgs()
        item_rel_msgs = self._pick_msgs_section(cabal_messages, r'item\d+')
        item_rel_msgs = self._add_itemKind(item_rel_msgs)
        item_rel_msgs = self._expand_item_ids(item_rel_msgs)

        return item_rel_msgs