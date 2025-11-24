import PyInstaller.__main__
import customtkinter
import os
import shutil

APP_NAME = "YTSorter"
MAIN_SCRIPT = "main.py"
ctk_path = os.path.dirname(customtkinter.__file__)

print("--- INICIANDO COMPILACIÓN ---")

# Limpieza
if os.path.exists("dist"): shutil.rmtree("dist")
if os.path.exists("build"): shutil.rmtree("build")
if os.path.exists(f"{APP_NAME}.spec"): os.remove(f"{APP_NAME}.spec")

# Configuración de assets (Fuente)
assets_arg = f'assets{os.pathsep}assets'

args = [
    MAIN_SCRIPT,
    f'--name={APP_NAME}',
    '--onefile',
    '--noconsole', # Quitar si deseas ver debug logs en el exe final
    '--clean',
    f'--add-data={ctk_path}{os.pathsep}customtkinter',
    f'--add-data={assets_arg}',
]

PyInstaller.__main__.run(args)
print(f"✅ COMPILACIÓN EXITOSA: dist/{APP_NAME}.exe")