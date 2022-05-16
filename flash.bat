@echo off

cd /D %~dp0
set filename="%~dp0dmaStuff\logs\flash\flash%date:~-4%-%date:~-7,2%-%date:~-10,2%--%time:~-11,2%-%time:~-8,2%-%time:~-5,2%.txt"

dir *.bin | find "1 File(s)" >NUL
cls

if errorlevel 1 (
	echo.
	echo.
	echo Error while looking for firmware file.
	echo Most likely no firmware file or multiple .bin files were found.
	echo Please make sure that there is only one firmware file next to the flash.bat.
	echo It needs to be a .bin file.
	echo.
	pause
	goto eof
) ELSE (
	if exist ".\dmaStuff\Ocd\firmware.bin" (
		move .\dmaStuff\Ocd\firmware.bin .\dmaStuff\Ocd\firmware%date:~-4%-%date:~-7,2%-%date:~-10,2%--%time:~-11,2%-%time:~-8,2%-%time:~-5,2%.bin >NUL
	)
	xcopy .\*.bin .\dmaStuff\Ocd\firmware.bin* >NUL
)

if exist ".\dmaStuff\Ocd\firmware.bin" (
	goto decision
) ELSE (
	echo Error while copying firmware file. No firmware.bin file found in destination.
	pause
	goto eof
)


cls
:decision

set /p flash=Are you sure that you want to flash your DMA Device? [Y/N]

if %flash%==Y goto flash
if %flash%==y goto flash
if %flash%==yes goto flash
if %flash%==Yes goto flash
if %flash%==YES goto flash

if %flash%==N goto eof
if %flash%==n goto eof
if %flash%==no goto eof
if %flash%==No goto eof
if %flash%==NO goto eof

echo.
echo.
echo Invlaid entry please enter "YES" or "NO". Your entry was "%flash%"
echo.
goto decision


:flash
cls
cd .\dmaStuff\Ocd\
openocd.exe -f flash_dma.cfg > %filename%
type %filename%

echo.
echo Log saved to %filename%

pause