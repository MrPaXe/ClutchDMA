@echo off

cd /D %~dp0

net session >NUL
if errorlevel 1 goto runAs
goto main

:runAs
powershell "start test.bat -v runAs"
exit

:main

::passing args
set mappingMode=%1


call ftdDriverInstall.bat
call dllPatch.bat

::actual test
echo.
echo Starting pcileech test.
echo.

cd .\pcileech\

if %mappingMode% == noMap (
	pcileech.exe -v -device fpga -min 0x100000 display 1> ..\testResult.tmp
	goto testResult
) 
if %mappingMode% == autoMap (
	pcileech.exe -v -device fpga -memmap auto -min 0x100000 display 1> ..\testResult.tmp
	goto testResult
)
if %mappingMode% == manualMap (
	pcileech.exe -v -device fpga -memmap ..\..\mmap.txt -min 0x100000 display 1> ..\testResult.tmp
	goto testResult
)

echo.
echo Invalid mapping mode. Contact support on the Clutch-Solution Discord.
echo Invalid mapping mode. Contact support on the Clutch-Solution Discord.
echo Invalid mapping mode. Contact support on the Clutch-Solution Discord.
echo.
pause
exit


:testResult
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

find /c "Invalid memory map: " .\testResult.tmp >Nul
if ERRORLEVEL 1 (
	echo.
) ELSE (
	del .\testResult.tmp
	echo. 
	echo Invalid or missing memory map!
	echo Invalid or missing memory map!
	echo Invalid or missing memory map!
	echo.
	echo.
	pause
	exit
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


echo.
echo Test results unkown. Please validate the results yourself or contact support staff on the Clutch-Solution discord.
echo Test results unkown. Please validate the results yourself or contact support staff on the Clutch-Solution discord.
echo Test results unkown. Please validate the results yourself or contact support staff on the Clutch-Solution discord.
del .\testResult.tmp
echo.
echo.
pause


:tinytestCheck
set /p tinytestCheck=BAD TEST: Try tiny test? [Y/N] 
IF NOT DEFINED tinytestCheck SET "tinytestCheck=Y"

if /I %tinytestCheck%==Y start tinytest.bat %mappingMode% -v runAs
if /I %tinytestCheck%==YES start tinytest.bat %mappingMode% -v runAs

exit

:end
pause
exit