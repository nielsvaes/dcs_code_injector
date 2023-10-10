
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & ".\venv\Scripts\activate.bat & python main.py" & Chr(34), 0
Set WshShell = Nothing