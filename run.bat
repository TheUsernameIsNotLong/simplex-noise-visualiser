@echo off

SET VENV_DIR=venv

IF NOT EXIST %VENV_DIR% (
    ECHO Creating virtual environment...
    call setup.bat
)

venv\Scripts\python.exe src\main.py
pause