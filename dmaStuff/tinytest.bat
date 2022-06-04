@echo off

cd /D %~dp0

::passing args
set mappingMode=%1

::actual test
echo.
echo Starting algo=3 test.
echo.

cd .\pcileech\

if %mappingMode% == noMap (
	pcileech.exe -v -device fpga://algo=3 -min 0x100000 display
) 
if %mappingMode% == autoMap (
	pcileech.exe -v -device fpga://algo=3 -memmap auto -min 0x100000 display
)
if %mappingMode% == manualMap (
	pcileech.exe -v -device fpga://algo=3 -memmap ..\..\mmap.txt -min 0x100000 display
)


echo.

:end
pause
exit