@echo off

cd /D %~dp0

::actual test
echo.
echo Starting algo=3 test.
echo.

cd .\pcileech\
pcileech.exe -v -device fpga://algo=3 -min 0x100000 display


echo.

:end
pause
exit