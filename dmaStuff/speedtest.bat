@echo off

::passing args
set mappingMode=%1

cd /D %~dp0

call ftdDriverInstall.bat
call dllPatch.bat

cd .\pcileech\

if %mappingMode% == noMap (
	pcileech.exe -v dump -device fpga -out none
	goto end
) 
if %mappingMode% == autoMap (
	pcileech.exe -v dump -device fpga -memmap auto -out none
	goto end
)
if %mappingMode% == manualMap (
	pcileech.exe -v dump -device fpga -memmap ..\..\mmap.txt -out none
	goto end
)

echo.
echo Invalid mapping mode. Contact support on the Clutch-Solution Discord.
echo Invalid mapping mode. Contact support on the Clutch-Solution Discord.
echo Invalid mapping mode. Contact support on the Clutch-Solution Discord.
echo.
pause
exit


:end
echo.
rundll32 user32.dll,MessageBeep
pause
exit