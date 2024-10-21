@echo off
cd ./
pyinstaller --onefile --windowed --icon=%~dp0icon.ico --specpath ./spec --name MotionUtils ./motion_utils_pac.py
pause