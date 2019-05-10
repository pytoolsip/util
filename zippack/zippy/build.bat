
@echo off && setlocal enabledelayedexpansion

set /p isLight=Do you ensure use the light mode?(y/n):

if %isLight%==y (
	python main.py light
) else (
	python main.py
)

pause