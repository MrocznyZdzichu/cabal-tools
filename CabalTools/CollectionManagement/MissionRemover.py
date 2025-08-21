from ..FileHandling.SCPData import SCPData


class MissionRemover:
    def __init__(self):
        pass

    def delete_mission(
        self,
        scp_data: SCPData,
        dec_data: dict,
        colle_tab_map: dict,
        mission_tab_map: dict,
        c_type: int,
        c_id: int,
        m_id: int,
    ):
        self._delete_mission_scp(
            scp_data, colle_tab_map, mission_tab_map, c_type, c_id, m_id
        )
        self._delete_mission_dec(dec_data, c_type, c_id, m_id)

    def _delete_mission_scp(self, scp_data: SCPData, colle_tab_map: dict, mission_tab_map: dict,
                            c_type: int, c_id: int, m_id: int):
        collection_entry_id = colle_tab_map.get((c_type, c_id, m_id))
        mission_entry_ids   = mission_tab_map.get((c_type, c_id, m_id), [])

        scp_data.remove_entry('Collection', collection_entry_id)
        for id in mission_entry_ids:
            scp_data.remove_entry('Mission', id)

        for section in ('Collection', 'Mission'):
            table = scp_data.get_section(section)
            for entry in table:
                if entry['c_type'] == c_type and entry['c_id'] == c_id and entry['mission_id'] > m_id:
                    entry['mission_id'] -= 1

    def _delete_mission_dec(self, dec_data: dict, c_type: int, c_id: int, m_id: int):
        c_type = str(c_type)
        c_id   = str(c_id)
        m_id   = str(m_id)

        # Collection_mission section
        for entry in dec_data['children'][2]['children']:
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

        # Collection_type section
        for entry in dec_data['children'][1]['children']:
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
