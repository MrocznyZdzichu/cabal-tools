import os
import json
from typing                             import Optional, cast, get_type_hints

from .FileHandling.FileBackuper         import FileBackuper
from .SpecificLoaders.SkillsDataLoader  import SkillsDataLoader
from .SpecificLoaders.ShopDataLoader    import ShopDataLoader
from .SpecificLoaders.ItemDataLoader    import ItemDataLoader
from .SpecificLoaders.WarpDataLoader    import WarpDataLoader
from .SpecificLoaders.ConstSCPLoader    import ConstSCPLoader

from .SkillsManagement.SkillManager     import SkillManager
from .NPCShopManagement.NPCShopManager  import NPCShopManager
from .WarpsManagement.WarpManager       import WarpManager
from .ConstManagement.ConstManager      import ConstManager


class CabalTools:
    # Tips for VSC tooltips
    SkillManager: Optional[SkillManager] = None
    ShopsManager: Optional[NPCShopManager] = None
    WarpManager: Optional[WarpManager] = None
    ConstManager: Optional[ConstManager] = None

    def __init__(self, config='config.json'):
        self.load_config(config=config)
        self._loader_configs = {
            "skills": {
                "class": SkillsDataLoader,
                "args": [
                    self._skill_dec_path,
                    self._cabal_messages_path,
                    self._skill_scp_path,
                    self._mb_scp_path,
                    self._pvp_scp_path
                ],
                "kwargs": {}
            },
            "shops": {
                "class": ShopDataLoader,
                "args": [],
                "kwargs": {
                    "npcshop_scp_path": self._npcshop_scp_path,
                    "cabal_messages_path": self._cabal_messages_path
                }
            },
            "items": {
                "class": ItemDataLoader,
                "args": [],
                "kwargs": {
                    "scp_path": self._item_scp_path,
                    "messages_path": self._cabal_messages_path
                }
            },
            "warp_points": {
                "class": WarpDataLoader,
                "args": [],
                "kwargs": {
                    "dec_path": self._warp_dec_path,
                    "scp_path": self._warp_scp_path
                }
            },
            "const_scp": {
                "class": ConstSCPLoader,
                "args": [],
                "kwargs": {
                    "scp_path": self._const_scp_path
                }
            },
        }
        self._manager_configs = [
            {
                "name": "SkillManager",
                "class": SkillManager,
                "loader": "_skills_dl",
                "unpack": True,
                "attr": "SkillManager"
            },
            {
                "name": "ShopsManager",
                "class": NPCShopManager,
                "loader": "_shops_dl",
                "extra_loaders": ["_items_dl"],
                "attr": "ShopsManager"
            },
            {
                "name": "WarpManager",
                "class": WarpManager,
                "loader": "_warp_points_dl",
                "unpack": True,
                "attr": "WarpManager"
            },
            {
                "name": "ConstManager",
                "class": ConstManager,
                "loader": "_const_scp_dl",
                "attr": "ConstManager"
            },
        ]
        
        # Tips for VSC tooltips
        self.SkillManager: SkillManager
        self.ShopsManager: NPCShopManager
        self.WarpManager: WarpManager
        self.ConstManager: ConstManager

        self._init_data_loaders()
        self._init_managers()
        self.FileBackuper = FileBackuper()

    def load_config(self, config='config.json'):
        print('Loading configuration ...')
        config = json.load(open(config, 'r'))
        self._scp_dir = config["scp-dir"]
        self._enc_dir = config["enc-dir"]
        self._lang_dir = config["lang-dir"]

        self._cabal_messages_path = os.path.join(self._lang_dir, 'cabal_msg.dec')

        self._skill_dec_path      = os.path.join(self._enc_dir,  'skill.dec')
        self._skill_scp_path      = os.path.join(self._scp_dir,  'Skill.scp')
        self._mb_scp_path         = os.path.join(self._scp_dir,  'MissionBattle.scp')
        self._pvp_scp_path        = os.path.join(self._scp_dir,  'PvPBattle.scp')

        self._npcshop_scp_path    = os.path.join(self._scp_dir,  'NPCShop.scp')
        self._item_scp_path       = os.path.join(self._scp_dir,  'Item.scp')

        self._warp_scp_path       = os.path.join(self._scp_dir,  'Warp.scp')
        self._warp_dec_path       = os.path.join(self._enc_dir,  'cabal.dec')
        
        self._const_scp_path      = os.path.join(self._scp_dir,  'Const.scp')

    def _init_data_loaders(self):
        print('Configuring data loaders ...')
        for name, cfg in self._loader_configs.items():
            print(f"Initializing {name} data loader ...", end='', flush=True)
            loader_cls = cfg["class"]
            loader_obj = loader_cls(*cfg["args"], **cfg["kwargs"])
            setattr(self, f"_{name}_dl", loader_obj)
            print(" Done!")

    def _init_managers(self):
        print("Configuring managers ...")
        for cfg in self._manager_configs:
            print(f"Initializing {cfg['name']} ...", end='', flush=True)
            loader = getattr(self, cfg["loader"])
            loaded_data = loader.load()

            if cfg.get("unpack", False):
                manager_obj = cfg["class"](*loaded_data)
            elif "extra_loaders" in cfg:
                shop_data, shop_msgs = loaded_data
                item_msgs = getattr(self, cfg["extra_loaders"][0]).load()
                manager_obj = cfg["class"](shop_data, shop_msgs, item_msgs)
            else:
                manager_obj = cfg["class"](loaded_data)

            setattr(self, cfg["attr"], manager_obj)
            print(" Done!")

    def backup_skill_files(self, bck_dir='Backups'):
        self.FileBackuper.make_a_backup(self._skill_dec_path,   backup_dir=bck_dir)
        self.FileBackuper.make_a_backup(self._skill_scp_path,   backup_dir=bck_dir)
        self.FileBackuper.make_a_backup(self._mb_scp_path,      backup_dir=bck_dir)
        self.FileBackuper.make_a_backup(self._pvp_scp_path,     backup_dir=bck_dir)

    def backup_npc_shops_files(self, bck_dir='Backups'):
        self.FileBackuper.make_a_backup(self._npcshop_scp_path, backup_dir=bck_dir)

    def backup_warp_files(self, bck_dir='Backups'):
        self.FileBackuper.make_a_backup(self._warp_dec_path, backup_dir=bck_dir)
        self.FileBackuper.make_a_backup(self._warp_scp_path, backup_dir=bck_dir)

    def backup_const_files(self, bck_dir='Backups'):
        self.FileBackuper.make_a_backup(self._const_scp_path, backup_dir=bck_dir)