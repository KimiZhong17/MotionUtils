@echo off
cd ./
pyinstaller --onefile --windowed --icon=%~dp0icon.ico --specpath ./spec ./bvh_utils_pac.py
pause