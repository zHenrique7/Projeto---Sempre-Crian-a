import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(
    name="aplicativo",
    version="1.0",
    description="aplicativo",
    executables=[Executable("aplicativo.py", base=base)],
    options={'build_exe': {
        'include_files': ['icone.ico', 'icon.png', 'lupa.png'],},},
)