@echo off

cd /D %~dp0
set filename="%~dp0dmaStuff\logs\test\test%date:~-4%-%date:~-7,2%-%date:~-10,2%--%time:~-11,2%-%time:~-8,2%-%time:~-5,2%.txt"

net session >NUL
if errorlevel 1 goto runAs
goto test

:runAs
powershell "start test.bat -v runAs"
goto eof

:test
::Auto driver install for DMA USB
pnputil /add-driver ".\dmaStuff\FTD3XXDriver_WHQLCertified_v1.3.0.4\x64\Win10\FTDIBUS3.inf" >NUL

if ERRORLEVEL 1 (
	echo.
	echo Failed to install USB driver.
	echo.
	goto end
) ELSE (
	echo.
	echo USB driver already existed or was successfully installed.
	echo.
)

::Auto dllPatch check and copy
for /f %%f in ('dir /b .\dmaStuff\Dllpatch\System32') do (
	IF EXIST C:\Windows\System32\%%f (
		echo %%f exists
	) ELSE (
		copy .\dmaStuff\Dllpatch\System32\%%f C:\Windows\System32\
		if ERRORLEVEL 1 (
			echo Failed to copy %%f , please insert manually.
		) ELSE (
			echo %%f Successfully copied.
		)
	)
)

for /f %%f in ('dir /b .\dmaStuff\Dllpatch\SysWOW64') do (
	IF EXIST C:\Windows\System32\%%f (
		echo %%f exists
	) ELSE (
		copy .\dmaStuff\Dllpatch\System32\%%f C:\Windows\System32\
		if ERRORLEVEL 1 echo Failed to copy %%f , please insert manually.
	)
)

::acutal test
echo.
echo Starting pcileech test.
echo.

cd .\dmaStuff\TestFiles\
pcileech.exe -v -device fpga -min 0x100000 display > %filename%
type %filename%

if ERRORLEVEL 1 (
	echo.
	echo Log could not be created.
) ELSE (
	echo.
	echo Log saved to %filename%
)

:end
pause