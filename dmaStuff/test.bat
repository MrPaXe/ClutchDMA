@echo off

cd /D %~dp0
set filename="%~dp0logs\test\test%date:~-4%-%date:~-7,2%-%date:~-10,2%--%time:~-11,2%-%time:~-8,2%-%time:~-5,2%.txt"
echo %filename%

net session >NUL
if errorlevel 1 goto runAs
goto test

:runAs
powershell "start test.bat -v runAs"
exit

:test
::Auto driver install for DMA USB
pnputil /add-driver ".\FTD3XXDriver_WHQLCertified_v1.3.0.4\x64\Win10\FTDIBUS3.inf" >NUL

if ERRORLEVEL 1 (
	echo.
	echo Failed to install USB driver.
	echo.
	goto end
) ELSE (
	echo.
	echo USB driver successfully installed.
	echo.
)

::Auto dllPatch check and copy
for /f %%f in ('dir /b .\Dllpatch\System32') do (
	IF EXIST C:\Windows\System32\%%f (
		echo %%f already exists.
	) ELSE (
		copy .\Dllpatch\System32\%%f C:\Windows\System32\
		if ERRORLEVEL 1 (
			echo Failed to copy %%f , please insert manually.
		) ELSE (
			echo %%f Successfully copied.
		)
	)
)

for /f %%f in ('dir /b .\Dllpatch\SysWOW64') do (
	IF EXIST C:\Windows\System32\%%f (
		echo %%f exists
	) ELSE (
		copy .\Dllpatch\System32\%%f C:\Windows\System32\
		if ERRORLEVEL 1 echo Failed to copy %%f , please insert manually.
	)
)

::actual test
echo.
echo Starting pcileech test.
echo.

cd .\pcileech\
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
exit