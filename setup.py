import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(
    name="Projeto_SC",
    version="1.0",
    description="Projeto_SC",
    executables=[Executable("Projeto_SC.py", base=base)],
    options={'build_exe': {
        'include_files': ['icone.ico', 'icon.png', 'lupa.png', 'atualizar.png', 'lixeira.png', 'voltar.png'],},},
)