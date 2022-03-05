import os
import sys
from distutils.core import setup
import cx_Freeze
import matplotlib

base = "Console"

executable = [
    cx_Freeze.Executable("main.py", base = base)
]

build_exe_options = {"includes":["matplotlib.backends.backend_tkagg"],
                     }

cx_Freeze.setup(
    name = "py",
    options = {"build_exe": build_exe_options},
    version = "0.0",
    description = "standalone",
    executables = executable
)