from .ABCSpecificLoader   import ABCSpecificLoader


class ItemDataLoader(ABCSpecificLoader):
    def __init__(self, scp_path, messages_path):
        super().__init__(
            scp_path=scp_path, 
            messages_path=messages_path, 
            msg_section_start='<item_msg>', 
            msg_section_end='</item_msg>'
        )
        self._upgrade_range      = list(range(0, 21))
        self._upgrade_multiplier = 8192

        self._bound_codes        = {
            0        : '',  
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

    def _prepare_item_msg_map(self, loaded_item_messages):
        return {x['ItemKind']: x for x in loaded_item_messages}

    def load(self):
        cabal_messages = self._load_msgs()
        item_rel_msgs = self._pick_msgs_section(cabal_messages, r'item\d+')
        item_rel_msgs = self._add_itemKind(item_rel_msgs)
        item_rel_msgs = self._expand_item_ids(item_rel_msgs)
        item_msg_dict = self._prepare_item_msg_map(item_rel_msgs)
        
        return item_rel_msgs, item_msg_dict
