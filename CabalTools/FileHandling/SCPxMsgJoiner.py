import copy


class SCPxMsgJoiner:
    def __init__(self):
        pass

    def join_scp_with_msg(self, scp, msg, scp_key, key_build_fun, msg_key, msg_val, new_idx_name):
        rich_scp = copy.deepcopy(scp)
        for section in rich_scp:
            if scp_key in section['entries'][0].keys():
                for entry in section['entries']:
                    if entry[scp_key]:
                        idx_text = key_build_fun(entry[scp_key])
                        found_message = [msg_entry[msg_val] for msg_entry in msg if msg_entry[msg_key] == idx_text]
                        entry[new_idx_name] = found_message[0] if len(found_message) > 0 and found_message[0] != '' else None
        return rich_scp