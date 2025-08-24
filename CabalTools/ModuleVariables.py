from .SpecificLoaders import *

from .SkillsManagement import SkillManager
from .NPCShopManagement import NPCShopManager
from .WarpsManagement import WarpManager
from .ConstManagement import ConstManager
from .MultipleSCPManagement import MultipleSCPManager
from .DropListManagement import DropListManager
from .CollectionManagement import CollectionManager
from .OVLManagement import OVLManager


def get_loader_config(paths):
    return {
        "skills": {
            "class": SkillsDataLoader,
            "args": [
                paths["_skill_dec_path"],
                paths["_cabal_messages_path"],
                paths["_skill_scp_path"],
                paths["_mb_scp_path"],
                paths["_pvp_scp_path"],
            ],
            "kwargs": {},
        },
        "shops": {
            "class": ShopDataLoader,
            "args": [],
            "kwargs": {
                "npcshop_scp_path": paths["_npcshop_scp_path"],
                "cabal_messages_path": paths["_cabal_messages_path"],
            },
        },
        "items": {
            "class": ItemDataLoader,
            "args": [],
            "kwargs": {
                "scp_path": paths["_item_scp_path"],
                "messages_path": paths["_cabal_messages_path"],
            },
        },
        "warp_points": {
            "class": WarpDataLoader,
            "args": [],
            "kwargs": {
                "dec_path": paths["_warp_dec_path"],
                "scp_path": paths["_warp_scp_path"],
            },
        },
        "const_scp": {
            "class": ConstSCPLoader,
            "args": [],
            "kwargs": {"scp_path": paths["_const_scp_path"]},
        },
        "multiple_scp": {
            "class": MultipleSCPLoader,
            "args": [],
            "kwargs": {"scp_path": paths["_multiple_scp_path"]},
        },
        "droplists": {
            "class": DropListLoader,
            "args": [],
            "kwargs": {"scp_path": paths["_drop_list_scp_path"]},
        },
        "mobs": {
            "class": MobsLoader,
            "args": [],
            "kwargs": {"messages_path": paths["_mobs_msg_path"]},
        },
        "worlds_msg": {
            "class": WorldMsgLoader,
            "args": [paths["_world_msg_path"]],
            "kwargs": {},
        },
        "forcecodes" : {
            "class": ForceCodeDictLoader,
            "args": [],
            "kwargs": {},
        },
        "collection": {
            "class": CollectionDataLoader,
            "args": [
                paths["_colle_scp_path"],
                paths["_colle_dec_path"],
                paths["_colle_msg_path"],
            ],
            "kwargs": {},
        },
        "ovl": {
            "class": OVLDataLoader,
            "args": [
                paths["_ovl_scp_path"],
                paths["_ovl_dec_path"],
                paths["_ovl_msg_path"],
            ],
            "kwargs": {},
        },
    }


def get_manager_config():
    return [
        {"name": "SkillManager", "class": SkillManager, "loader": "_skills_dl", "attr": "SkillManager"},
        {"name": "ShopsManager", "class": NPCShopManager, "loader": "_shops_dl", "attr": "ShopsManager", "extra_loaders": ["_items_dl"], "unpack": False},
        {"name": "WarpManager", "class": WarpManager, "loader": "_warp_points_dl", "attr": "WarpManager"},
        {"name": "ConstManager", "class": ConstManager, "loader": "_const_scp_dl", "attr": "ConstManager"},
        {"name": "MultipleManager", "class": MultipleSCPManager, "loader": "_multiple_scp_dl", "attr": "MultipleManager"},
        {"name": "DropListManager", "class": DropListManager, "loader": "_droplists_dl", "attr": "DropListManager", "extra_loaders": ["_mobs_dl", "_worlds_msg_dl", "_items_dl"]},
        {"name": "CollectionManager", "class": CollectionManager, "loader": "_collection_dl", "attr": "CollectionManager", "extra_loaders": ["_items_dl", "_forcecodes_dl"]},
        {"name": "OVLManager", "class": OVLManager, "loader": "_ovl_dl", "attr": "OVLManager", "extra_loaders" : ["_forcecodes_dl"]},
    ]


def get_backup_map(paths):
    return {
        "skills": [
            paths["_skill_dec_path"],
            paths["_skill_scp_path"],
            paths["_mb_scp_path"],
            paths["_pvp_scp_path"],
        ],
        "npc_shops": [paths["_npcshop_scp_path"]],
        "warps": [paths["_warp_dec_path"], paths["_warp_scp_path"]],
        "const": [paths["_const_scp_path"]],
        "multiple": [paths["_multiple_scp_path"]],
        "world_drops": [paths["_drop_list_scp_path"]],
        "collection": [
            paths["_colle_scp_path"],
            paths["_colle_dec_path"],
            paths["_colle_msg_path"],
        ],
        "ovl" : [paths["_ovl_scp_path"], paths["_ovl_dec_path"], paths["_ovl_msg_path"]]
    }
