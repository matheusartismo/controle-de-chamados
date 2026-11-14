@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel% equ 0 (
    py -3 app.py
) else (
    where python >nul 2>&1
    if errorlevel 1 (
        echo Instale o Python em https://www.python.org/downloads/ e tente novamente.
    ) else (
        python app.py
    )
)
pause
