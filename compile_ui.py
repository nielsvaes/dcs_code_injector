import os
import subprocess
from ez_utils import file_utils


folder = os.path.dirname(__file__)
pyside6uic_exe = os.path.join(folder, "venv", "Scripts", "pyside6-uic.exe")

for ui_path in file_utils.get_files_recursively(folder, filters=[".ui"]):
    compiled_path = ui_path.replace(".ui", ".py")
    command = "%s %s > %s" % (pyside6uic_exe, ui_path, compiled_path)
    print(command)
    subprocess.Popen(command, shell=True)