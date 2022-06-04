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