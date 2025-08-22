class MissionAdder:
    @staticmethod
    def add_scp_colle_sec(scp_data, c_type, c_id, reward_type, reward_id, c_reward_id):
        entries = scp_data.get_section('Collection')
        new_entries = []

        ids = [x['mission_id'] for x in entries if x['c_type'] == c_type and x['c_id'] == c_id]
        if ids == []:
            m_id = 1
        else:
            m_id = max([x['mission_id'] for x in entries if x['c_type'] == c_type and x['c_id'] == c_id]) + 1

        idx  = max([x['RowIndex'] for x in entries]) + 1

        new_record = {
            'RowIndex'      : idx,
            'c_type'        : c_type,
            'c_id'          : c_id,
            'mission_id'    : m_id,    
            'm_reward_type' : reward_type,
            'm_reward_id'   : reward_id,
            'c_reward_id'   : c_reward_id,
        }

        entry_added = False

        for entry in entries:
            if not entry_added and entry.get('c_type') == c_type and entry.get('c_id') > c_id:
                new_entries.append(new_record)
                entry_added = True

            new_entries.append(entry)

            if not entry_added and entry.get('c_type') == c_type and entry.get('c_id') == c_id and entry.get('mission_id') == m_id - 1:
                new_entries.append(new_record)
                entry_added = True

        entries.clear()
        entries.extend(new_entries)

    @staticmethod
    def add_scp_mission_sec(scp_data, c_type, c_id, slots_config):
        entries = scp_data.get_section('Mission')
        new_entries = []

        ids = [x['mission_id'] for x in entries if x['c_type'] == c_type and x['c_id'] == c_id]
        if ids == []:
            m_id = 1
        else:
            m_id = max([x['mission_id'] for x in entries if x['c_type'] == c_type and x['c_id'] == c_id]) + 1
        idx  = max([x['RowIndex'] for x in entries]) + 1

        prev_mission_found = False
        mission_added      = False

        for entry in entries:            
            if (
                (entry.get('c_type') == c_type and entry.get('c_id') == c_id and entry.get('mission_id') == m_id - 1)
                or (entry.get('c_type') == c_type and entry.get('c_id') == c_id + 1 and not prev_mission_found)
            ):
                prev_mission_found = True
            if not (entry.get('c_type') == c_type and entry.get('c_id') == c_id) and prev_mission_found and not mission_added:
                for slot_id, slot_properties in enumerate(slots_config):
                    new_record = {
                        'RowIndex'    : idx + slot_id,
                        'c_type'      : c_type,
                        'c_id'        : c_id,
                        'mission_id'  : m_id,
                        'slot_id'     : slot_id,
                        'm_item_type' : slot_properties['m_item_type'],
                        'm_item_id'   : slot_properties['m_item_id'],
                        'm_item_need' : slot_properties['m_item_need'],
                    }
                    new_entries.append(new_record)
                mission_added = True
            new_entries.append(entry)

        entries.clear()
        entries.extend(new_entries)

    @staticmethod
    def add_dec_colle_sec(dec_data, c_type, c_id, reward_type, reward_id, c_reward_id):
        for entry in dec_data['children'][1]['children']:
            ct = entry['attributes']['type']
            if ct == c_type:
                for entry2 in entry['children']:
                    cid  = entry2['attributes']['c_id']
                    crid = entry2['attributes']['c_reward_id']
                    if cid == c_id and crid == c_reward_id:
                        ids = [int(x['attributes']['mission_id']) for x in entry2['children']]
                        if ids == []:
                            m_id = "1"
                        else:
                            m_id = str(max([int(x['attributes']['mission_id']) for x in entry2['children']]) + 1)
                        new_entry = {'tag' : 'collection_detail', 'attributes' : {
                            'mission_id' : m_id, 'm_reward_type' : reward_type, 'm_reward_id' : reward_id
                        }}
                        entry2['children'].append(new_entry)

    @staticmethod
    def _convert_slots_to_str(slots_config):
        for d in slots_config:
            for k in d.keys():
                d[k] = str(d[k])
        return slots_config

    @staticmethod
    def _get_next_mission_id(entry, c_id):
        ids = [int(x["attributes"]["mission_id"]) for x in entry["children"] if x["attributes"]["c_id"] == c_id]
        if ids == []:
            return "1"
        else:
            return str(
                max(
                    [
                        int(x["attributes"]["mission_id"])
                        for x in entry["children"]
                        if x["attributes"]["c_id"] == c_id
                    ]
                ) + 1
            )

    @staticmethod
    def _build_mission_entry(c_id, mission_id, slots_config):
        new_entry = {
            "tag": "mission_info",
            "attributes": {"c_id": c_id, "mission_id": mission_id},
            "children": [],
        }

        for it, slot in enumerate(slots_config):
            new_entry["children"].append(
                {
                    "tag": "mission_detail",
                    "attributes": {
                        "slot_id": str(it),
                        "m_item_type": slot["m_item_type"],
                        "m_item_id": slot["m_item_id"],
                        "m_item_need": slot["m_item_need"],
                    },
                }
            )
        return new_entry

    @staticmethod
    def add_dec_mission_sec(dec_data, c_type, c_id, slots_config):
        slots_config = MissionAdder._convert_slots_to_str(slots_config)

        colle_found = False
        entry_added = False
        new_entries = []

        for entry in dec_data["children"][2]["children"]:
            ct = entry["attributes"]["c_type"]
            if ct == c_type:
                m_id = MissionAdder._get_next_mission_id(entry, c_id)
                new_entry = MissionAdder._build_mission_entry(c_id, m_id, slots_config)

                for entry2 in entry["children"]:
                    cid = entry2["attributes"]["c_id"]
                    mid = entry2["attributes"]["mission_id"]
                    if not entry_added and int(cid) == int(c_id) + 1:
                        new_entries.append(new_entry)
                        entry_added = True

                    if cid == c_id:
                        colle_found = True
                    new_entries.append(entry2)

                    if int(mid) == int(m_id) - 1 and colle_found and not entry_added:
                        new_entries.append(new_entry)
                        entry_added = True
                
                entry['children'].clear()
                entry['children'].extend(new_entries)
                
    @staticmethod
    def add_mission(scp_data, dec_data, c_type, c_id, reward_type, reward_id, c_reward_id, slots_config):
        MissionAdder.add_scp_colle_sec(scp_data, c_type, c_id, reward_type, reward_id, c_reward_id)
        MissionAdder.add_scp_mission_sec(scp_data, c_type, c_id, slots_config)
        MissionAdder.add_dec_colle_sec(dec_data, str(c_type), str(c_id), str(reward_type), str(reward_id), str(c_reward_id))
        MissionAdder.add_dec_mission_sec(dec_data, str(c_type), str(c_id), slots_config)
