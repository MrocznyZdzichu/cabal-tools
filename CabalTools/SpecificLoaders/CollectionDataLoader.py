from .ABCSpecificLoader import ABCSpecificLoader


class CollectionDataLoader(ABCSpecificLoader):
    def __init__(
        self,
        scp_path,
        dec_path,
        messages_path,
    ):
        super().__init__(
            scp_path,
            dec_path,
            messages_path,
            dec_section_start='<Collection>',
            dec_section_end='</Collection>',
            msg_section_start='<Collection_message>',
            msg_section_end='</Collection_message>',
        )

    def _build_collection_type_dict(self):
        return {
            1 : 'Dungeons',
            2 : 'Maps',
            3 : 'Special',
            4 : 'Event',
            5 : 'Ruler Bosses'
        }

    def _build_collection_name_dict(self, msg_data):
        c_id_dict = {}
        type_info = msg_data['children'][0]['children']
        for type in type_info:
            t_id = type['attributes']['t_id']
            for collection in type['children']:
                c_id = collection['attributes']['c_id']
                name = collection['attributes']['name']
                c_id_dict[str(t_id)+'--'+str(c_id)] = name
        return c_id_dict

    def _build_mission_name_dict(self, msg_data):
        m_id_dict = {}
        type_info = msg_data['children'][1]['children']
        for type in type_info:
            t_id = type['attributes']['t_id']
            for collection in type['children']:
                c_id = collection['attributes']['c_id']
                m_id = collection['attributes']['m_id']
                name = collection['attributes']['name']
                m_id_dict[str(t_id)+'--'+str(c_id)+'--'+str(m_id)] = name

        return m_id_dict

    def _build_reward_type_dict(self):
        return {
            1 : 'Force Gems',
            2 : 'Item'
        }

    def _build_item_type_dict(self) -> dict:
        return {
            1 : "Straight item",
            2 : "Upgraded item",
            4 : "Stackable item",
        }

    def _build_item_name_dict(self, msg_data) -> dict:
        return {
            (x['attributes']['type_id'], x['attributes']['item_id']) : x['attributes']['name']
                for x in msg_data['children'][2]['children']
        }

    def load(self):
        scp_data = self._load_scp_file()
        dec_data = self._load_dec()
        msg_data = self._load_msgs()

        c_type_dict = self._build_collection_type_dict()
        c_id_dict   = self._build_collection_name_dict(msg_data)
        m_id_dict   = self._build_mission_name_dict(msg_data)
        r_type_dict = self._build_reward_type_dict()
        item_type   = self._build_item_type_dict()
        item_name   = self._build_item_name_dict(msg_data)

        return (
            scp_data,
            dec_data,
            msg_data,
            c_type_dict,
            c_id_dict,
            m_id_dict,
            r_type_dict,
            item_type,
            item_name,
        )
