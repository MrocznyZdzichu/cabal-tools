import os
import json

from .FileBackuper     import FileBackuper

from .SkillChanger     import SkillChanger
from .SkillsDataLoader import SkillsDataLoader

class CabalTools:
    def __init__(self, config='config.json'):
        self.load_config(config=config)
        self.load_skill_changer()
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

    def load_skill_changer(self):
        sdl = SkillsDataLoader(
            self._skill_dec_path,
            self._cabal_messages_path,
            self._skill_scp_path,
            self._mb_scp_path,
            self._pvp_scp_path
        )
        cabal_skill_names, skill_details_dict, skill_scp_data, skill_mb_data, skill_pvp_data = sdl.load()
        self.SkillChanger = SkillChanger(
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