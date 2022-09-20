@echo off

cd /D %~dp0
set flashMode=%1


set x=1
set i=0
for %%a in (..\*.bin) do set /a i+=1

cls

if %i% EQU %x% (
	if exist ".\Ocd\firmware.bin" (
		move ".\Ocd\firmware.bin" ".\Ocd\firmware%date:~-4%-%date:~-7,2%-%date:~-10,2%--%time:~-11,2%-%time:~-8,2%-%time:~-5,2%.bin" >NUL
	)
	xcopy ..\*.bin .\Ocd\firmware.bin* >NUL
) ELSE (
	echo.
	echo Error while looking for firmware file.
	echo Most likely no firmware file or multiple .bin files were found.
	echo Please make sure that there is only one firmware file next to the dma.bat.
	echo It needs to be a .bin file.
	echo.
	pause
	exit
)

if exist ".\Ocd\firmware.bin" (
	goto decision
) ELSE (
	echo Error while copying firmware file. No firmware.bin file found in destination.
	pause
	exit
)


cls
:decision

set /p flash=Are you sure that you want to flash your DMA Device? [Y/N] 
IF NOT DEFINED flash SET "flash=Y"

if /I %flash%==Y goto flash
if /I %flash%==YES goto flash

if /I %flash%==N exit
if /I %flash%==NO exit

echo.
echo.
echo Invlaid entry please enter "YES" or "NO". Your entry was "%flash%"
echo.
goto decision


:flash
cls

cd .\Ocd\

if %flashMode% == defaultVID_PID goto defaultVID_PID
if %flashMode% == customVID_PID goto customVID_PID

echo.
echo Invalid flashing mode. Contact support on the Clutch-Solution Discord.
echo Invalid flashing mode. Contact support on the Clutch-Solution Discord.
echo Invalid flashing mode. Contact support on the Clutch-Solution Discord.
echo.
pause
exit

:defaultVID_PID
openocd.exe -f openocdDefault.cfg

echo.
pause

:customVID_PID
cls
:customVID_PIDSetting

echo Enter your custom VID in the following formatting: 
echo 0x0403
set /p customVID=
cls

echo Enter your custom PID in the following formatting: 
echo 0x6011
set /p customPID=

cls
echo VID: %customVID%
echo PID: %customPID%
echo.

set /p confirmCustomVIDPID=Continue? [Y/N] 
IF NOT DEFINED confirmCustomVIDPID SET "confirmCustomVIDPID=Y"

if /I %confirmCustomVIDPID%==Y goto customVID_PIDFlash
if /I %confirmCustomVIDPID%==YES goto customVID_PIDFlash

if /I %confirmCustomVIDPID%==N goto customVID_PIDSetting
if /I %confirmCustomVIDPID%==NO goto customVID_PIDSetting

:customVID_PIDFlash
echo interface ftdi > openocdCustom_%customVID%_%customPID%.cfg
echo ftdi_vid_pid %customVID% %customPID% >> openocdCustom_%customVID%_%customPID%.cfg
echo ftdi_channel 0 >> openocdCustom_%customVID%_%customPID%.cfg
echo ftdi_layout_init 0x0098 0x008b >> openocdCustom_%customVID%_%customPID%.cfg
echo reset_config none >> openocdCustom_%customVID%_%customPID%.cfg
echo source xilinx-xc7.cfg >> openocdCustom_%customVID%_%customPID%.cfg
echo source jtagspi.cfg >> openocdCustom_%customVID%_%customPID%.cfg
echo adapter_khz 10000 >> openocdCustom_%customVID%_%customPID%.cfg
echo proc fpga_program {} { >> openocdCustom_%customVID%_%customPID%.cfg
echo 	global _CHIPNAME >> openocdCustom_%customVID%_%customPID%.cfg
echo 	xc7_program $_CHIPNAME.tap >> openocdCustom_%customVID%_%customPID%.cfg
echo } >> openocdCustom_%customVID%_%customPID%.cfg
echo init >> openocdCustom_%customVID%_%customPID%.cfg
echo jtagspi_init 0 bscan_spi_xc7a35t.bit >> openocdCustom_%customVID%_%customPID%.cfg
echo jtagspi_program firmware.bin 0x0 >> openocdCustom_%customVID%_%customPID%.cfg
echo fpga_program >> openocdCustom_%customVID%_%customPID%.cfg
echo shutdown >> openocdCustom_%customVID%_%customPID%.cfg

pause

openocd.exe -f openocdCustom_%customVID%_%customPID%.cfg

echo.
pause
