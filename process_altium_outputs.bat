@echo off
setlocal

REM === Set project path here ===
set "PROJECT_DIR=C:\Users\julia\OneDrive\Projekte\PCBs\multi_sensor_core\Project Outputs for multi_sensor_core"

REM === Call Python script ===
python "%~dp0process_jlcpcb_outputs.py" "%PROJECT_DIR%"

pause
