@echo off

cd /D %~dp0

net session >NUL
if errorlevel 1 goto runAs
goto main

:runAs
powershell "start test.bat -v runAs"
exit

:main

call %~dp0ftdDriverInstall.bat
call %~dp0dllPatch.bat

::actual test
echo.
echo Starting pcileech test.
echo.

cd .\pcileech\
pcileech.exe -v -device fpga -memmap auto -min 0x100000 display 1> ..\testResult.tmp
cd ..\

type .\testResult.tmp
echo.

::check for test results

find /c "DEVICE: FPGA: ERROR: Unable to connect to USB/FT601 device [0,v0.0,0000]" .\testResult.tmp >Nul
if ERRORLEVEL 1 (
	echo.
) ELSE (
	del .\testResult.tmp
	echo.
	echo No USB Connection to DMA Device! 
	echo Make sure that the USB is plugged in the DATA USB-Port.
	echo Try changing the USB-Port on the Radar-PC.
	echo.
	echo.
	
	pause
	exit
)
	
find /c "Memory Display: Failed reading memory at address: " .\testResult.tmp >Nul
if ERRORLEVEL 1 (
	echo.
) ELSE (
	del .\testResult.tmp
	goto tinytestCheck
)

find /c "Memory Display: Contents for address: " .\testResult.tmp >Nul
if ERRORLEVEL 1 (
	echo.
) ELSE (
	del .\testResult.tmp
	echo.
	echo Good test result!
	echo Good test result!
	echo Good test result!
	echo.
	echo.
	
	pause
	exit
)

del .\testResult.tmp
echo.
echo Test results unkown. Please validate yourself or contact support staff on the Clutch-Solution discord.
echo Test results unkown. Please validate yourself or contact support staff on the Clutch-Solution discord.
echo Test results unkown. Please validate yourself or contact support staff on the Clutch-Solution discord.
echo.
echo.
pause


:tinytestCheck
set /p tinytestCheck=BAD TEST: Try tiny test? [Y/N] 
IF NOT DEFINED tinytestCheck SET "tinytestCheck=Y"

if /I %tinytestCheck%==Y start tinytest.bat -v runAs
if /I %tinytestCheck%==YES start tinytest.bat -v runAs

if /I %flash%==N exit
if /I %flash%==NO exit

echo.
echo.
echo Invlaid entry please enter "YES" or "NO". Your entry was "%flash%"
echo.
goto tinytestCheck


:end
pause
exit