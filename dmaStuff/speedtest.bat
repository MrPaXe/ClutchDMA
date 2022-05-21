@echo off

cd /D %~dp0

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
			echo Failed to copy %%f from Dllpatch\System32, please insert manually.
		) ELSE (
			echo %%f Successfully copied.
		)
	)
)

for /f %%f in ('dir /b .\Dllpatch\SysWOW64') do (
	IF EXIST C:\Windows\SysWOW64\%%f (
		echo %%f already exists.
	) ELSE (
		copy .\Dllpatch\SysWOW64\%%f C:\Windows\SysWOW64\
		if ERRORLEVEL 1 (
			echo Failed to copy %%f from Dllpatch\SysWOW64, please insert manually.
		) ELSE (
			echo %%f Successfully copied.
		)
	)
)

cd .\pcileech\
pcileech.exe -v -vv -device fpga -out none dump

echo.

pause
exit