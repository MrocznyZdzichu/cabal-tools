import os
import json

from .FileHandling.FileBackuper         import FileBackuper
from .SpecificLoaders.SkillsDataLoader  import SkillsDataLoader
from .SpecificLoaders.ShopDataLoader    import ShopDataLoader
from .SpecificLoaders.ItemDataLoader    import ItemDataLoader
from .SpecificLoaders.WarpDataLoader    import WarpDataLoader

from .SkillsManagement.SkillManager     import SkillManager
from .NPCShopManagement.NPCShopManager  import NPCShopManager
from .WarpsManagement.WarpManager       import WarpManager


class CabalTools:
    def __init__(self, config='config.json'):
        self.load_config(config=config)
        self._init_data_loaders()
        self._load_skill_manager()
        self._load_npc_manager()
        self._load_warp_manager()
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

    def _init_data_loaders(self):
        print('Configuring data loaders ...')
        self._skills_dl = SkillsDataLoader(
            self._skill_dec_path,
            self._cabal_messages_path,
            self._skill_scp_path,
            self._mb_scp_path,
            self._pvp_scp_path
        )
        self._shops_dl = ShopDataLoader(
            npcshop_scp_path    = self._npcshop_scp_path, 
            cabal_messages_path = self._cabal_messages_path
        )
        self._items_dl = ItemDataLoader(
            scp_path      = self._item_scp_path, 
            messages_path = self._cabal_messages_path
        )
        self._warp_points_dl = WarpDataLoader(
            dec_path = self._warp_dec_path,
            scp_path = self._warp_scp_path
        )

    def _load_skill_manager(self):
        print('Loading skill-related data ...')
        cabal_skill_names, skill_details_dict, skill_scp_data, skill_mb_data, skill_pvp_data = self._skills_dl.load()
        print('Starting SkillManager module ...')
        self.SkillManager = SkillManager(
            skill_names    = cabal_skill_names, 
            skill_details  = skill_details_dict, 
            skill_scp_data = skill_scp_data, 
            mb_sc_data     = skill_mb_data, 
            pvp_scp_data   = skill_pvp_data
        )

    def _load_npc_manager(self):
        print('Loading shops-related data ...')
        npcshop_scp_data, npc_rel_msgs = self._shops_dl.load()
        print('Loading items-related messages ...')
        item_rel_msgs = self._items_dl.load()

        print('Starting ShopsManager module ...')
        self.ShopsManager = NPCShopManager(npcshop_scp_data, npc_rel_msgs, item_rel_msgs)

    def _load_warp_manager(self):
        print('Load Warp Points data ...')
        warp_dec_data, warp_scp_data = self._warp_points_dl.load()

        print('Starting WarpMangager module ...')
        self.WarpManager = WarpManager(warp_dec_data, warp_scp_data)

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