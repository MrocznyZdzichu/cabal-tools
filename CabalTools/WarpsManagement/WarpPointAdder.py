import copy


class WarpPointAdder:
    def __init__(self):
        self._dec_ordered_keys = [
            "x", "y",
            "nation1x", "nation1y",
            "nation2x", "nation2y",
            "nation3x", "nation3y",
            "w_code", "Fee", "WorldIdx", "level"
        ]

    def _remap_scp_attributes(self, warp_point_item, next_row_index):
        new_entry = {
            "RowIndex":        next_row_index,
            "WorldIdx":        int(warp_point_item.WorldIdx),
            "ProcessIdx":      0,
            "PosXPnt":         int(warp_point_item.x),
            "PosYPnt":         int(warp_point_item.y),
            "Nation1PosXPnt":  int(warp_point_item.nation1x),
            "Nation1PosYPnt":  int(warp_point_item.nation1y),
            "Nation2PosXPnt":  int(warp_point_item.nation2x),
            "Nation2PosYPnt":  int(warp_point_item.nation2y),
            "Nation3PosXPnt":  int(warp_point_item.nation3x),
            "Nation3PosYPnt":  int(warp_point_item.nation3y),
            "LV":              int(warp_point_item.level),
            "Fee":             int(warp_point_item.Fee),
            "W_code":          int(warp_point_item.w_code),
        }
        return new_entry
    
    def _process_dec(self, dec_data, warp_point_item):
        new_dec = copy.deepcopy(dec_data)

        attributes = {k: getattr(warp_point_item, k) for k in self._dec_ordered_keys}

        new_child = {
            "tag": "warp_index",
            "attributes": attributes
        }
        new_dec.setdefault("children", []).append(new_child)

        return new_dec
        
    def _process_scp(self, scp_data, warp_point_item):
        new_scp = copy.deepcopy(scp_data)

        warp_section = next((s for s in new_scp if s.get("section") == "Warp"), None)
        if warp_section is None:
            return new_scp

        entries = warp_section.setdefault("entries", [])
        next_row_index = entries[-1]["RowIndex"] + 1 if entries else 0

        new_entry = self._remap_scp_attributes(warp_point_item, next_row_index)
        entries.append(new_entry)

        return new_scp

    def add_warp_point(self, dec_data, scp_data, warp_point_item):
        new_dec = self._process_dec(dec_data, warp_point_item)
        new_scp = self._process_scp(scp_data, warp_point_item)
        
        return new_dec, new_scp