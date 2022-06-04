@echo off

cd /D %~dp0

call %~dp0ftdDriverInstall.bat
call %~dp0dllPatch.bat

cd .\pcileech\
pcileech.exe dump -device fpga -memmap auto -out none

echo.
rundll32 user32.dll,MessageBeep
pause
exit