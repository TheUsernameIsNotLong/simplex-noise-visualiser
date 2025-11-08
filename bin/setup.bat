@echo off

SET VENV_DIR=venv

IF NOT EXIST "%VENV_DIR%" (
    ECHO Creating virtual environment...
    python -m venv "%VENV_DIR%"
) ELSE (
    ECHO Virtual environment already exists.
)

call "%VENV_DIR%\Scripts\activate"

python -m pip install --upgrade pip

IF EXIST "requirements.txt" (
    ECHO Installing dependencies...
    pip install -r requirements.txt
) ELSE (
    ECHO requirements.txt not found!
)

echo Setup complete!
