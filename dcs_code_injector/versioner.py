import stat
import os
import shutil
import datetime

LOCAL_HISTORY = ".local_history"
AUTO_PREFIX = ".version__"
NAMED_PREFIX = ".named__"
READONLY = 33060
WRITABLE = 33206


def auto_backup_file(file_path, amount_of_back_ups=5):
    """
    Makes a copy of the file to a folder next to the file

    :param file_path: *string*
    :param amount_of_back_ups: *int* Oldest backup gets deleted if you're saving more than this number
    :return: *bool* if the operation was a success
    """
    if not os.path.isfile(file_path):
        return False

    folder = os.path.dirname(file_path)
    old_file_name = os.path.basename(file_path)
    new_file_name = AUTO_PREFIX + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + "__" + old_file_name

    complete_folder_path = os.path.join(folder, LOCAL_HISTORY)
    if not os.path.isdir(complete_folder_path):
        os.makedirs(complete_folder_path)

    existing_versions = [os.path.join(complete_folder_path, file) for file in os.listdir(complete_folder_path)
                         if os.path.isfile(os.path.join(complete_folder_path, file))
                         and file.startswith(AUTO_PREFIX) and old_file_name in file]

    existing_versions.sort()

    while len(existing_versions) >= amount_of_back_ups:
        delete_file = existing_versions.pop(0)
        os.remove(delete_file)

    shutil.copyfile(file_path, os.path.join(complete_folder_path, new_file_name))

    return True

def named_backup_file(original_file_path, custom_file_name):
    """
    Makes a copy of a file to a folder next to the file. Doesn't add a timestamp to it

    :param original_file_path: *string* Complete path of file that needs backing up, eg: D:/folder/game/my_animation.fbx
    :param custom_file_name: *string* name of the file, without extension, eg: my_animation_fixed
    :return:
    """
    old_file_name = os.path.basename(original_file_path)
    folder = os.path.dirname(original_file_path)
    complete_folder_path = os.path.join(folder, LOCAL_HISTORY)
    complete_backup_file_path = os.path.join(NAMED_PREFIX + custom_file_name + "__" + old_file_name)

    if not os.path.isdir(complete_folder_path):
        os.makedirs(complete_folder_path)

    shutil.copyfile(original_file_path, os.path.join(complete_folder_path, complete_backup_file_path))

def auto_backup_folder(folder_path, amount_of_back_ups=10):
    """
    Backs up an entire folder by calling backup_file for every file in it.

    :param folder_path: *string*
    :param amount_of_back_ups: *int* Oldest backup gets deleted if you're saving more than this number
    :return:
    """
    if not os.path.isdir(folder_path):
        return False

    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path)
                  if os.path.isfile(os.path.join(folder_path, file))]

    for file_path in file_paths:
        auto_backup_file(file_path, amount_of_back_ups=amount_of_back_ups)

    return True

def list_backups_of_file(file_path, auto=True, named=True):
    """
    Returns a list of all the previous versions of file_path

    :param file_path: *string*
    :param auto: *bool* return automatically made backups
    :param named: *bool* return explicitly named backups
    :return: *list*
    """
    if not os.path.isfile(file_path):
        return []

    folder = os.path.dirname(file_path)
    old_file_name = os.path.basename(file_path)

    complete_folder_path = os.path.join(folder, LOCAL_HISTORY)

    backups = []
    if os.path.isdir(complete_folder_path):
        if auto:
            backups.extend([os.path.join(complete_folder_path, file) for file in os.listdir(complete_folder_path)
                            if os.path.isfile(os.path.join(complete_folder_path, file))
                            and file.startswith(AUTO_PREFIX) and old_file_name in file])
        if named:
            backups.extend([os.path.join(complete_folder_path, file) for file in os.listdir(complete_folder_path)
                             if os.path.isfile(os.path.join(complete_folder_path, file))
                             and file.startswith(NAMED_PREFIX) and old_file_name in file])
        backups.sort()
    return backups


def restore_auto_backup(backup_file_path):
    """
    Renames the backup file to its original name and copies it one folder up

    :param backup_file_path: *string* complete path to backup file eg D:/folder/files/.local_history/.version__2020-11-26-09-40-19__myfile.json
    :return:
    """
    original_folder = os.path.dirname(os.path.dirname(backup_file_path))
    original_file = "__".join(os.path.basename(backup_file_path).split("__")[2:]) # just in case there as a __ in the OG file path
    complete_original_file_path = os.path.join(original_folder, original_file)

    mode = READONLY

    try:
        if os.path.isfile(complete_original_file_path):
            # keep readonly status on the file if needed
            mode = os.stat(complete_original_file_path).st_mode
            os.chmod(complete_original_file_path, stat.S_IWRITE)

        shutil.copyfile(backup_file_path, complete_original_file_path)

        if mode == READONLY:
            os.chmod(complete_original_file_path, stat.S_IREAD)

        return True
    except Exception as err:
        print(str(err))
        return False

def restore_named_backup(backup_file_path, original_file_path):
    """
    Copies the backup file over the original file

    :param backup_file_path: *string* complete path to backup file eg D:/folder/files/.local_history/.version__2020-11-26-09-40-19__myfile.json
    :param original_file_path: *string* complete path to where the backup needs to be copied to
    :return:
    """
    mode = READONLY

    try:
        if os.path.isfile(original_file_path):
            mode = os.stat(original_file_path).st_mode
            os.chmod(original_file_path, stat.S_IWRITE)

        shutil.copyfile(backup_file_path, original_file_path)

        if mode == READONLY:
            os.chmod(original_file_path, stat.S_IREAD)

        return True
    except Exception as err:
        print(str(err))
        return False