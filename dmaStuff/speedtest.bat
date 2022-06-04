@echo off

::passing args
set mappingMode=%1

cd /D %~dp0

call %~dp0ftdDriverInstall.bat
call %~dp0dllPatch.bat

cd .\pcileech\

if %mappingMode% == noMap (
	pcileech.exe dump -device fpga -out none
) 
if %mappingMode% == autoMap (
	pcileech.exe dump -device fpga -memmap auto -out none
)
if %mappingMode% == manualMap (
	pcileech.exe dump -device fpga -memmap ..\..\mmap.txt -out none
)

echo.
rundll32 user32.dll,MessageBeep
pause
exit