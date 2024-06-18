from cx_Freeze import setup, Executable
import sys
import os

# Obter o diretório onde o script está localizado
base_dir = os.path.dirname(os.path.abspath(__file__))

# Definir o base como "Win32GUI" para aplicativos GUI no Windows
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="Projeto_SC",
    version="1.0",
    description="Projeto_SC",
    executables=[Executable("Projeto_SC.py", base=base, icon=os.path.join(base_dir, 'icone.ico'))],
    options={
        'build_exe': {
            'include_files': [
                os.path.join(base_dir, 'icone.ico'),
                os.path.join(base_dir, 'icon.png'),
                os.path.join(base_dir, 'lupa.png'),
                os.path.join(base_dir, 'atualizar.png'),
                os.path.join(base_dir, 'lixeira.png'),
                os.path.join(base_dir, 'voltar.png'),
            ],
            'includes': ['sqlite3'],  # Incluir o módulo sqlite3
        },
    },
)
