@echo off
setlocal

REM === Ask user for project path ===
set /p PROJECT_DIR="Enter the project path: "

REM === Call Python script ===
python "%~dp0process_jlcpcb_outputs.py" "%PROJECT_DIR%"

pause
