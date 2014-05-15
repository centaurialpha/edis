"""
Recursos

"""

import os

PATH = os.path.abspath(os.path.dirname(__file__))

# Iconos
ICONOS = {
    "nuevo": os.path.join(PATH, "imagenes", "nuevo.png"),
    "abrir": os.path.join(PATH, "imagenes", "abrir.png"),
    "guardar": os.path.join(PATH, "imagenes", "guardar.png"),
    "guardar-como": os.path.join(PATH, "imagenes", "guardar.png"),
    "salir": os.path.join(PATH, "imagenes", "salir.png"),
    "logo": os.path.join(PATH, "imagenes", "logo.png"),
    "icono": os.path.join(PATH, "imagenes", "icono.png"),
    "print": os.path.join(PATH, "imagenes", "print.png")}

# Estilos de color
COLOR_TEMA = {
    "editor": "#1d1f21"
    }