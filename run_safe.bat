@echo off
REM Helper to run safe_run.py with full python path (adjust if your Python is elsewhere)
"C:\Users\misha\AppData\Local\Programs\Python\Python313\python.exe" "%~dp0safe_run.py" "%~dp0examples\physics.conf" "%~dp0examples\physics.xml"
if exist "%~dp0examples\physics.xml" (
  echo Generated: %~dp0examples\physics.xml
  type "%~dp0examples\physics.xml"
) else (
  echo Physics generation failed; check error.log
  if exist "%~dp0error.log" type "%~dp0error.log"
)

"C:\Users\misha\AppData\Local\Programs\Python\Python313\python.exe" "%~dp0safe_run.py" "%~dp0examples\server.conf" "%~dp0examples\server.xml"
if exist "%~dp0examples\server.xml" (
  echo Generated: %~dp0examples\server.xml
  type "%~dp0examples\server.xml"
) else (
  echo Server generation failed; check error.log
  if exist "%~dp0error.log" type "%~dp0error.log"
)

pause
