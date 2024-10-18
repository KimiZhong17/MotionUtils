@echo off
cd ./
pyinstaller --onefile --windowed --icon=%~dp0icon.ico --specpath ./bvh_utils ./bvh_utils/combine_bvh_pac.py
pause