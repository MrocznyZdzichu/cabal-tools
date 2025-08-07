class FileBackuper:
    def __init__(self):
        pass

    def make_a_backup(self, file_path, backup_dir='Backups'):
        import os
        import shutil
        import datetime

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file_name = f"{os.path.basename(file_path)}_{timestamp}.bak"
        backup_file_path = os.path.join(backup_dir, backup_file_name)

        shutil.copy2(file_path, backup_file_path)
        return backup_file_path