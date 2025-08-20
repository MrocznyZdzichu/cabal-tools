import os
import json
from typing import Optional

from .FileHandling.FileBackuper import FileBackuper

from .SpecificLoaders import *
from .SkillsManagement import *
from .NPCShopManagement import *
from .WarpsManagement import *
from .ConstManagement import *
from .MultipleSCPManagement import *
from .DropListManagement import *


class CabalTools:
    # Tips for VSC tooltips
    SkillManager: Optional[SkillManager] = None
    ShopsManager: Optional[NPCShopManager] = None
    WarpManager: Optional[WarpManager] = None
    ConstManager: Optional[ConstManager] = None
    MultipleManager: Optional[MultipleSCPManager] = None
    DropListManager: Optional[DropListManager] = None

    def __init__(self, config="config.json", modules=None):
        # Tips for VSC tooltips
        self.SkillManager: SkillManager
        self.ShopsManager: NPCShopManager
        self.WarpManager: WarpManager
        self.ConstManager: ConstManager
        self.MultipleManager: MultipleSCPManager
        self.DropListManager: DropListManager

        self._modules_loaded = modules
        self.load_config(config=config)
        self.FileBackuper = FileBackuper()

    def load_config(self, config="config.json"):
        print("Loading configuration ...")
        config = json.load(open(config, "r"))
        self._scp_dir = config["scp-dir"]
        self._enc_dir = config["enc-dir"]
        self._lang_dir = config["lang-dir"]

        self._cabal_messages_path = os.path.join(self._lang_dir, "cabal_msg.dec")

        self._skill_dec_path = os.path.join(self._enc_dir, "skill.dec")
        self._skill_scp_path = os.path.join(self._scp_dir, "Skill.scp")
        self._mb_scp_path = os.path.join(self._scp_dir, "MissionBattle.scp")
        self._pvp_scp_path = os.path.join(self._scp_dir, "PvPBattle.scp")

        self._npcshop_scp_path = os.path.join(self._scp_dir, "NPCShop.scp")
        self._item_scp_path = os.path.join(self._scp_dir, "Item.scp")

        self._warp_scp_path = os.path.join(self._scp_dir, "Warp.scp")
        self._warp_dec_path = os.path.join(self._enc_dir, "cabal.dec")

        self._const_scp_path = os.path.join(self._scp_dir, "Const.scp")
        self._multiple_scp_path = os.path.join(self._scp_dir, "Multiple.scp")

        self._drop_list_scp_path = os.path.join(self._scp_dir, "World_drop.scp")
        self._mobs_msg_path = os.path.join(self._lang_dir, "cabal_msg.dec")
        self._world_msg_path = os.path.join(self._lang_dir, "cabal_msg.dec")

        self._loader_configs = self._prepare_loaders_config()
        self._manager_configs = self._prepare_managers_config()

        self._init_data_loaders()
        self._init_managers()

    def _prepare_loaders_config(self):
        return {
            "skills": {
                "class": SkillsDataLoader,
                "args": [
                    self._skill_dec_path,
                    self._cabal_messages_path,
                    self._skill_scp_path,
                    self._mb_scp_path,
                    self._pvp_scp_path,
                ],
                "kwargs": {},
            },
            "shops": {
                "class": ShopDataLoader,
                "args": [],
                "kwargs": {
                    "npcshop_scp_path": self._npcshop_scp_path,
                    "cabal_messages_path": self._cabal_messages_path,
                },
            },
            "items": {
                "class": ItemDataLoader,
                "args": [],
                "kwargs": {
                    "scp_path": self._item_scp_path,
                    "messages_path": self._cabal_messages_path,
                },
            },
            "warp_points": {
                "class": WarpDataLoader,
                "args": [],
                "kwargs": {
                    "dec_path": self._warp_dec_path,
                    "scp_path": self._warp_scp_path,
                },
            },
            "const_scp": {
                "class": ConstSCPLoader,
                "args": [],
                "kwargs": {"scp_path": self._const_scp_path},
            },
            "multiple_scp" : {
                "class": MultipleSCPLoader,
                "args" : [],
                "kwargs" : {
                    "scp_path" : self._multiple_scp_path
                }
            },
            "droplists" : {
                "class": DropListLoader,
                "args" : [],
                "kwargs" : {
                    "scp_path" : self._drop_list_scp_path
                }
            },
            "mobs" : {
                "class": MobsLoader,
                "args" : [],
                "kwargs" : {
                    "messages_path" : self._mobs_msg_path
                }
            },
            "worlds_msg" : {
                "class": WorldMsgLoader,
                "args" : [self._world_msg_path],
                "kwargs" : {}
            },
        }

    def _prepare_managers_config(self):
        modules = [
            {
                "name": "SkillManager",
                "class": SkillManager,
                "loader": "_skills_dl",
                "attr": "SkillManager",
            },
            {
                "name": "ShopsManager",
                "attr": "ShopsManager",
                "class": NPCShopManager,
                "loader": "_shops_dl",
                "extra_loaders": ["_items_dl"],
                "unpack": False,
            },
            {
                "name": "WarpManager",
                "class": WarpManager,
                "loader": "_warp_points_dl",
                "attr": "WarpManager",
            },
            {
                "name": "ConstManager",
                "class": ConstManager,
                "loader": "_const_scp_dl",
                "attr": "ConstManager",
            },
            {
                "name": "MultipleManager",
                "class": MultipleSCPManager,
                "loader": "_multiple_scp_dl",
                "attr": "MultipleManager"
            },
            {
                "name": "DropListManager",
                "class": DropListManager,
                "loader": "_droplists_dl",
                "extra_loaders": ["_mobs_dl", "_worlds_msg_dl", "_items_dl"],
                "attr": "DropListManager"
            },
        ]
        return modules if not self._modules_loaded else [module for module in modules if module['name'] in self._modules_loaded]

    def _init_data_loaders(self):
        print("Configuring data loaders ...")
        for name, cfg in self._loader_configs.items():
            print(f"\tInitializing {name} data loader ...", end="", flush=True)
            loader_cls = cfg["class"]
            loader_obj = loader_cls(*cfg["args"], **cfg["kwargs"])
            setattr(self, f"_{name}_dl", loader_obj)
            print(" Done!")

    def _get_or_load(self, loader_name, loader_obj):
        if loader_name not in self._loaded_cache:
            self._loaded_cache[loader_name] = loader_obj.load()
        return self._loaded_cache[loader_name]

    def _init_managers(self):
        print("Configuring managers ...")
        self._loaded_cache = {}

        for cfg in self._manager_configs:
            print(f"\tInitializing {cfg['name']} ...", end="", flush=True)

            loader_obj = getattr(self, cfg["loader"])
            loaded_data = self._get_or_load(cfg["loader"], loader_obj)

            if not isinstance(loaded_data, tuple):
                loaded_data = (loaded_data,)

            extra_data = []
            for extra_loader_name in cfg.get("extra_loaders", []):
                extra_loader_obj = getattr(self, extra_loader_name)
                extra_loaded = self._get_or_load(extra_loader_name, extra_loader_obj)

                if not isinstance(extra_loaded, tuple):
                    extra_loaded = (extra_loaded,)
                extra_data.extend(extra_loaded)

            manager_obj = cfg["class"](*loaded_data, *extra_data)
            setattr(self, cfg["name"], manager_obj)
            print(" Done!")

    def backup_skill_files(self, bck_dir="Backups"):
        self.FileBackuper.make_a_backup(self._skill_dec_path, backup_dir=bck_dir)
        self.FileBackuper.make_a_backup(self._skill_scp_path, backup_dir=bck_dir)
        self.FileBackuper.make_a_backup(self._mb_scp_path, backup_dir=bck_dir)
        self.FileBackuper.make_a_backup(self._pvp_scp_path, backup_dir=bck_dir)

    def backup_npc_shops_files(self, bck_dir="Backups"):
        self.FileBackuper.make_a_backup(self._npcshop_scp_path, backup_dir=bck_dir)

    def backup_warp_files(self, bck_dir="Backups"):
        self.FileBackuper.make_a_backup(self._warp_dec_path, backup_dir=bck_dir)
        self.FileBackuper.make_a_backup(self._warp_scp_path, backup_dir=bck_dir)

    def backup_const_files(self, bck_dir="Backups"):
        self.FileBackuper.make_a_backup(self._const_scp_path, backup_dir=bck_dir)

    def backup_multiple_scp_file(self, bck_dir="Backups"):
        self.FileBackuper.make_a_backup(self._multiple_scp_path, backup_dir=bck_dir)

    def backup_world_drops(self, bck_dir='Backups'):
        self.FileBackuper.make_a_backup(self._drop_list_scp_path, backup_dir=bck_dir)