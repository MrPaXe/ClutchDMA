@echo off

set ver="2.05"
cd /D %~dp0

del ver.txt >Nul
del updateHelper.bat >Nul

:adminCheck
net session >NUL
if errorlevel 1 goto runAs
goto autoUpdate

:runAs
powershell "start dma.bat -v runAs"
exit


:autoUpdate
echo.
echo Checking for updated ClutchDMA version...
echo.

curl http://clutch.paxe.at/ClutchDMA/ver.txt -J -O
find /c %ver% .\ver.txt >Nul

if ERRORLEVEL 1 (
	del ver.txt
	goto update
) ELSE (
	del ver.txt
	goto startLoop
)


:startLoop
cls

echo ClutchDMA %ver%
echo.
echo [1] Test
echo [2] Flash
echo [3] Speedtest
echo [4] Quit
echo.
echo [9] Update ClutchDMA files.
echo.


set /p choice=What do you want to do: 

cd .\dmaStuff\

if %choice%==1 start test.bat -v runAs
if %choice%==2 start flash.bat -v runAs
if %choice%==3 start speedtest.bat -v runAs
if %choice%==9 goto update
if %choice%==4 exit

goto StartLoop



:update
cls
set /p updateYN=Do you want to update your CltuchDMA files? (Highly recommended) [Y/N]
IF NOT DEFINED updateYN SET "updateYN=Y"
if /I %updateYN%==N goto startLoop

cd /D %~dp0
del updateHelper.bat

curl -O "http://clutch.paxe.at/ClutchDMA/updateHelper.bat"
start updateHelper.bat