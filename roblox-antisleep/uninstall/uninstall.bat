@echo off
echo Удаление программы...
taskkill /f /im main.py >nul 2>&1

REM Удаление из автозагрузки
reg delete "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsUpdateSvc" /f >nul 2>&1

REM Удаление файлов программы
del "%~dp0main.py" >nul 2>&1

REM Удаление папки программы
rmdir "%~dp0" >nul 2>&1

echo Программа успешно удалена.
pause