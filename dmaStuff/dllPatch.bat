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