import cx_Freeze
import sys
import PyQt5 
import matplotlib
import numpy

base = None

if sys.platform == 'win32':
    base = "Win32GUI"
#										filename
executables = [cx_Freeze.Executable("runge_kutta_gui.py", base=base)]

cx_Freeze.setup(
name = "Runge-Kutta-4",
options = {"build_exe": {"packages":["PyQt5","matplotlib","numpy",]}},
version = "1.0",
description = "Runge-Kutta method witth gui",
executables = executables
)