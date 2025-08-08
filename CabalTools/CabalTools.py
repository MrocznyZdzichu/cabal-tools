import os
import json

from .FileBackuper     import FileBackuper
from .SkillsDataLoader import SkillsDataLoader
from .ShopDataLoader   import ShopDataLoader
from .ItemDataLoader   import ItemDataLoader

from .SkillManager     import SkillManager


class CabalTools:
    def __init__(self, config='config.json'):
        self.load_config(config=config)
        self._init_data_loaders()
        self._load_skill_manager()
        self.FileBackuper = FileBackuper()

    def load_config(self, config='config.json'):
        config = json.load(open('config.json', 'r'))
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

    def _init_data_loaders(self):
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

    def _load_skill_manager(self):
        cabal_skill_names, skill_details_dict, skill_scp_data, skill_mb_data, skill_pvp_data = self._skills_dl.load()
        self.SkillManager = SkillManager(
            skill_names=cabal_skill_names, 
            skill_details=skill_details_dict, 
            skill_scp_data=skill_scp_data, 
            mb_sc_data=skill_mb_data, 
            pvp_scp_data=skill_pvp_data
        )

    def backup_skill_files(self, bck_dir='Backups'):
        self.FileBackuper.make_a_backup(self._skill_dec_path, backup_dir=bck_dir)
        self.FileBackuper.make_a_backup(self._skill_scp_path, backup_dir=bck_dir)
        self.FileBackuper.make_a_backup(self._mb_scp_path, backup_dir=bck_dir)
        self.FileBackuper.make_a_backup(self._pvp_scp_path, backup_dir=bck_dir)