import copy


class SCPxMsgJoiner:
    def __init__(self):
        pass

    def join_scp_with_msg(self, scp, msg, scp_key, key_build_fun, msg_key, msg_val):
        rich_scp = copy.deepcopy(scp)
        for section in rich_scp:
            if scp_key in section['entries'][0].keys():
                for entry in section['entries']:
                    if entry[scp_key]:
                        idx_text = key_build_fun(entry[scp_key])
                        entry[scp_key] = [msg_entry[msg_val] for msg_entry in msg if msg_entry[msg_key] == idx_text][0]
        return rich_scp