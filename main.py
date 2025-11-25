import subprocess
import os
import click


@click.group()
def menu_principal():
    """Menú principal para seleccionar el entorno"""
    pass


def activar_entorno_y_ejecutar(virtual_env_path, script_path, args):
    """Activa el entorno virtual y ejecuta el script dado."""
    # Convertir rutas a absolutas
    virtual_env_path = os.path.abspath(virtual_env_path)
    script_path = os.path.abspath(script_path)

    # Determinar el directorio base del script
    script_dir = os.path.dirname(script_path)
    if os.name == "nt":  # Windows
        activate_script = os.path.join(virtual_env_path, "Scripts", "activate.bat")
        command = f'cmd /c "cd {script_dir} & {activate_script} & python {os.path.basename(script_path)} {" ".join(args)}"'
    else:  # Linux/Mac
        activate_script = os.path.join(virtual_env_path, "bin", "activate")
        command = f'cd {script_dir} && source {activate_script} && python {os.path.basename(script_path)} {" ".join(args)}'

    try:
        # Ejecutar el comando para activar el entorno y ejecutar el script
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el script: {e}")


@menu_principal.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("args", nargs=-1)
def roblox(args):
    """Ejecutar el script principal de Roblox"""
    print("Ejecutando el entorno de Roblox...")
    activar_entorno_y_ejecutar(
        virtual_env_path="Roblox/.venv", script_path="Roblox/mainroblox.py", args=args
    )


@menu_principal.command(context_settings=dict(ignore_unknown_options=True))
@click.argument("args", nargs=-1)
def steam(args):
    """Ejecutar el script principal de Steam"""
    print("Ejecutando el entorno de Steam...")
    activar_entorno_y_ejecutar(
        virtual_env_path="Steam/.venv", script_path="Steam/main.py", args=args
    )


if __name__ == "__main__":
    menu_principal()
