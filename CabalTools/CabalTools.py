import os
import json
from typing import Optional

from .FileHandling.FileBackuper import FileBackuper
from .ModuleVariables import get_loader_config, get_manager_config, get_backup_map

from .SkillsManagement import SkillManager
from .NPCShopManagement import NPCShopManager
from .WarpsManagement import WarpManager
from .ConstManagement import ConstManager
from .MultipleSCPManagement import MultipleSCPManager
from .DropListManagement import DropListManager
from .CollectionManagement import CollectionManager
from .OVLManagement import OVLManager
from .StellarManagement import StellarManager

class CabalTools:
    # Tips for VSC tooltips
    SkillManager:      Optional[SkillManager]       = None
    ShopsManager:      Optional[NPCShopManager]     = None
    WarpManager:       Optional[WarpManager]        = None
    ConstManager:      Optional[ConstManager]       = None
    MultipleManager:   Optional[MultipleSCPManager] = None
    DropListManager:   Optional[DropListManager]    = None
    CollectionManager: Optional[CollectionManager]  = None
    OVLManager:        Optional[OVLManager]         = None
    StellarManager:    Optional[StellarManager]     = None

    def __init__(self, config="config.json", modules=None):
        # Tips for VSC tooltips
        self.SkillManager: SkillManager
        self.ShopsManager: NPCShopManager
        self.WarpManager: WarpManager
        self.ConstManager: ConstManager
        self.MultipleManager: MultipleSCPManager
        self.DropListManager: DropListManager
        self.CollectionManager: CollectionManager
        self.OVLManager: OVLManager
        self.StellarManager: StellarManager

        self._modules_loaded = modules
        self.load_config(config=config)
        self.FileBackuper = FileBackuper()

    def load_config(self, config="config.json"):
        print("Loading configuration ...")
        config = json.load(open(config, "r"))
        self._scp_dir = config["scp-dir"]
        self._enc_dir = config["enc-dir"]
        self._lang_dir = config["lang-dir"]

        self._set_config_files_paths()

        self._loader_configs = get_loader_config(vars(self))
        self._manager_configs = (
            get_manager_config()
            if not self._modules_loaded
            else [m for m in get_manager_config() if m["name"] in self._modules_loaded]
        )
        self._backup_map = get_backup_map(vars(self))

        self._init_data_loaders()
        self._init_managers()

    def _set_config_files_paths(self):
        self._cabal_messages_path = os.path.join(self._lang_dir, "cabal_msg.dec")

        self._skill_dec_path = os.path.join(self._enc_dir, "skill.dec")
        self._skill_scp_path = os.path.join(self._scp_dir, "Skill.scp")
        self._mb_scp_path = os.path.join(self._scp_dir, "MissionBattle.scp")
        self._pvp_scp_path = os.path.join(self._scp_dir, "PvPBattle.scp")

        self._npcshop_scp_path = os.path.join(self._scp_dir, "NPCShop.scp")
        self._item_scp_path = os.path.join(self._scp_dir, "Item.scp")

        self._warp_scp_path = os.path.join(self._scp_dir, "Warp.scp")
        self._warp_dec_path = os.path.join(self._enc_dir, "cabal.dec")

        self._const_scp_path    = os.path.join(self._scp_dir, "Const.scp")
        self._multiple_scp_path = os.path.join(self._scp_dir, "Multiple.scp")

        self._drop_list_scp_path = os.path.join(self._scp_dir, "World_drop.scp")
        self._mobs_msg_path      = os.path.join(self._lang_dir, "cabal_msg.dec")
        self._world_msg_path     = os.path.join(self._lang_dir, "cabal_msg.dec")

        self._colle_scp_path = os.path.join(self._scp_dir, "Collection.scp")
        self._colle_dec_path = os.path.join(self._enc_dir, "Collection.dec")
        self._colle_msg_path = os.path.join(self._lang_dir, "Collection_msg.dec")

        self._ovl_scp_path = os.path.join(self._scp_dir, "Overloadmastery.scp")
        self._ovl_dec_path = os.path.join(self._enc_dir, "overloadmastery.dec")
        self._ovl_msg_path = os.path.join(self._lang_dir, "overloadmastery_msg.dec")
        
        self._stellar_scp_path = os.path.join(self._scp_dir, "Stellar.scp")
        self._stellar_dec_path = os.path.join(self._enc_dir, "stellar.dec")
        self._stellar_msg_path = os.path.join(self._lang_dir, "stellar_msg.dec")

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

    def backup(self, category: str, bck_dir="Backups"):
        if category not in self._backup_map:
            raise ValueError(f"Unknown backup category: {category}")
        for path in self._backup_map[category]:
            self.FileBackuper.make_a_backup(path, backup_dir=bck_dir)
