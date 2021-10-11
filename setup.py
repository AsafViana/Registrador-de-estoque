import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
        Executable("main.py", base=base, icon='modulos\icon\icon.ico', target_name='Registros')
]

buildOptions = dict(
        packages = [],
        includes = ['PyQt5', "reportlab.pdfgen", 'modulos', 'pyautogui'],
        include_files = [],
)

setup(
    name = "Registro",
    version = "1.0",
    description = "registra itens",
    options = dict(build_exe = buildOptions),
    executables = executables
 )
