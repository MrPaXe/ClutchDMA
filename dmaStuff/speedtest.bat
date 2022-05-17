@echo off

cd .\pcileech\
pcileech.exe -v -vv -device fpga -out none dump

echo.

pause
exit