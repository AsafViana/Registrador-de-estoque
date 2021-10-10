import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
        Executable("main.py", base=base, icon='icon.ico', target_name='Registros')
]

buildOptions = dict(
        packages = [],
        includes = ['PyQt5', "reportlab.pdfgen", 'modulos.arquivo', 'modulos.banco', 'pyautogui'],
        include_files = ['formulario.ui', 'listar_dados.ui', 'menu_editar.ui', r'modulos\icon\registro.png'],
)

setup(
    name = "Registro",
    version = "1.0",
    description = "registra itens",
    options = dict(build_exe = buildOptions),
    executables = executables
 )
