cls
@echo off
title Form converter

:SETUP
echo Enter form name to convert into .py (without .ui):
echo Type 'exit' to exit
set/p "name=> "
if %name%==exit goto EXIT
pyuic5 %name%.ui -o %name%.py
goto SETUP

:EXIT