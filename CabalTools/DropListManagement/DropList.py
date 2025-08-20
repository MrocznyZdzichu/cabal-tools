from collections import defaultdict

class DropList:
    def __init__(self, drop_items: list):
        self._droplist = drop_items

    def _get_group_key(self, item):
        if type(item).__name__ == "CommonDrop":
            return (item.WorldIdx,)
        elif type(item).__name__ == "MobDrop":
            return (item.WorldIdx, item.SpeciesIdx)
        elif type(item).__name__ == "BoxDrop":
            return (item.WorldIdx, item.DungeonID, item.BoxIdx)
        else:
            raise ValueError(f"Unsupported drop type: {type(item).__name__}")

    def normalize_droprates(self, normalize_to=100):
        groups = defaultdict(list)
        for item in self._droplist:
            groups[self._get_group_key(item)].append(item)

        for group_key, items in groups.items():
            total = sum(x.DropRate for x in items)
            if total == 0:
                continue
            factor = total / normalize_to
            for item in items:
                item.DropRate = item.DropRate / factor

    def __iter__(self):
        return iter(self._droplist)

    def __len__(self):
        return len(self._droplist)

    def __getitem__(self, index):
        return self._droplist[index]

# class DropList:
#     def __init__(self, drop_items: list):
#         self._droplist = drop_items
        
#     def normalize_droprates(self, normalize_to=100):
#         factor = float(sum([x.DropRate for x in self._droplist]))/normalize_to
#         for item in self._droplist:
#             item.DropRate = float(item.DropRate)/factor

#     def __iter__(self):
#         return iter(self._droplist)

#     def __len__(self):
#         return len(self._droplist)

#     def __getitem__(self, index):
#         return self._droplist[index]