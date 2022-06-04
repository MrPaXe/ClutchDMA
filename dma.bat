@echo off

set ver="2.07"
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
::check if website down.
if ERRORLEVEL 1 (
	echo Update server seems to be down. Please open a Ticket in the Clutch-Soution Discord.
	del ver.txt
	pause
	exit
)

find /c %ver% .\ver.txt >Nul

if ERRORLEVEL 1 (
	del ver.txt
	goto update
) ELSE (
	del ver.txt
	goto menuLoop
)


:menuLoop
cls

echo ClutchDMA %ver%
echo.
echo [1] Test
echo [2] Flash
echo [3] Speedtest
echo.
echo [9] Advanced
echo [0] Quit
echo.


set /p choice=What do you want to do: 

cd .\dmaStuff\

if %choice%==1 start test.bat noMap -v runAs
if %choice%==2 start flash.bat -v runAs
if %choice%==3 start speedtest noMap.bat -v runAs
if %choice%==9 goto advancedMenu
if %choice%==0 exit

goto menuLoop

:advancedMenu
::clears the variable
set "choice="

cls
echo ClutchDMA %ver%
echo.
echo Advanced Menu
echo.
echo [1] Test with automapping
echo [2] Test with manual map
echo.
echo [3] Speedtest with automapping
echo [4] Speedtest with manual map
echo.
echo [8] Update ClutchDMA files.
echo [9] Go back.
echo [0] Quit
echo.

set /p choice=What do you want to do: 

cd .\dmaStuff\

if %choice%==1 start test.bat autoMap -v runAs
if %choice%==2 start test.bat manualMap -v runAs
if %choice%==3 start speedtest.bat autoMap -v runAs
if %choice%==4 start speedtest.bat manualMap -v runAs
if %choice%==8 goto update
if %choice%==9 goto menuLoop
if %choice%==0 exit

goto menuLoop

:update
cls
set /p updateYN=Do you want to update your CltuchDMA files? (Highly recommended) [Y/N]
IF NOT DEFINED updateYN SET "updateYN=Y"
if /I %updateYN%==N goto menuLoop

cd /D %~dp0
del updateHelper.bat

curl -O "http://clutch.paxe.at/ClutchDMA/updateHelper.bat"

::check if website down.
if ERRORLEVEL 1 (
	echo Update server seems to be down. Please open a Ticket in the Clutch-Soution Discord.
	del updateHelper.txt
	pause
	exit
)

start updateHelper.bat
exit