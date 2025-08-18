from .ABCSpecificLoader   import ABCSpecificLoader
import copy

# class ItemDataLoader(ABCSpecificLoader):
#     def __init__(self, scp_path, messages_path):
#         super().__init__(
#             scp_path, 
#             messages_path, 
#             '<item_msg>', 
#             '</item_msg>'
#         )
#         self._upgrade_range      = list(range(1, 21))
#         self._upgrade_multiplier = 8192

#         self._bound_codes        = {
#             # 0       : '',
#             4096    : 'Account Bound',
#             524288  : 'Character Bound',
#             1572864 : 'Char. Bound on Equip'
#         }

#     def _add_itemKind(self, loaded_item_messages):
#         for entry in loaded_item_messages:
#             entry["ItemKind"] = int(entry["id"].replace("item", ""))
#         return loaded_item_messages
    
#     def _expand_item_ids(self, loaded_item_messages):
#         expanded_item_messages = loaded_item_messages

#         acc_bound_items = copy.deepcopy(loaded_item_messages)
#         for message in acc_bound_items:
#             message['ItemKind'] += 4096
#             message['cont'] += ' (Account Bound)'
#             message['id'] = f'item{message['ItemKind']}'
#         expanded_item_messages += acc_bound_items

#         char_bound_items = copy.deepcopy(loaded_item_messages)
#         for message in char_bound_items:
#             message['ItemKind'] += 524288
#             message['cont'] += ' (Character Bound)'
#             message['id'] = f'item{message['ItemKind']}'
#         expanded_item_messages += char_bound_items

#         on_equip_bound_items = copy.deepcopy(loaded_item_messages)
#         for message in on_equip_bound_items:
#             message['ItemKind'] += 1572864
#             message['cont'] += ' (Character Bound on Equip)'
#             message['id'] = f'item{message['ItemKind']}'
#         expanded_item_messages += char_bound_items

#         items_with_bound_codes = copy.deepcopy(expanded_item_messages)

#         for grade in self._upgrade_range:
#             items_at_grade = copy.deepcopy(items_with_bound_codes)
#             for message in items_at_grade:
#                 message['ItemKind'] += grade * self._upgrade_multiplier
#                 message['cont'] += f' + {grade}'
#                 message['id'] = f'item{message['ItemKind']}'
            
#             expanded_item_messages += items_at_grade

 
#         return expanded_item_messages

#     def load(self):
#         # scp_data = self._load_scp_file() Item.scp is useless for me so far so it is kept as a mock
#         cabal_messages = self._load_msgs()
#         item_rel_msgs = self._pick_msgs_section(cabal_messages, r'item\d+')
#         item_rel_msgs = self._add_itemKind(item_rel_msgs)
#         item_rel_msgs = self._expand_item_ids(item_rel_msgs)

#         return item_rel_msgs

class ItemDataLoader(ABCSpecificLoader):
    def __init__(self, scp_path, messages_path):
        super().__init__(
            scp_path, 
            messages_path, 
            '<item_msg>', 
            '</item_msg>'
        )
        self._upgrade_range      = list(range(0, 21))  # uwzględnij też +0
        self._upgrade_multiplier = 8192

        self._bound_codes        = {
            0        : '',  # brak binda
            4096     : 'Account Bound',
            524288   : 'Character Bound',
            1572864  : 'Char. Bound on Equip'
        }

    def _add_itemKind(self, loaded_item_messages):
        for entry in loaded_item_messages:
            entry["ItemKind"] = int(entry["id"].replace("item", ""))
        return loaded_item_messages
    
    def _expand_item_ids(self, loaded_item_messages):
        expanded = []
        for entry in loaded_item_messages:
            base_kind = entry["ItemKind"]
            base_name = entry["cont"]

            for bound_code, bound_label in self._bound_codes.items():
                for grade in self._upgrade_range:
                    item = entry.copy()
                    item["ItemKind"] = base_kind + bound_code + grade * self._upgrade_multiplier
                    suffix = []
                    if bound_label:
                        suffix.append(f"({bound_label})")
                    if grade > 0:
                        suffix.append(f"+{grade}")
                    if suffix:
                        item["cont"] = f"{base_name} {' '.join(suffix)}"
                    item["id"] = f"item{item['ItemKind']}"
                    expanded.append(item)

        return expanded

    def load(self):
        cabal_messages = self._load_msgs()
        item_rel_msgs = self._pick_msgs_section(cabal_messages, r'item\d+')
        item_rel_msgs = self._add_itemKind(item_rel_msgs)
        item_rel_msgs = self._expand_item_ids(item_rel_msgs)
        return item_rel_msgs
