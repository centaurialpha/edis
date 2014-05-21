"""
Recursos

"""

import os

PATH = os.path.abspath(os.path.dirname(__file__))
TEMA_SIDE = os.path.join(PATH, "temas", "tema_side.qss")
TEMA_POR_DEFECTO = os.path.join(PATH, "temas", "tema_por_defecto.qss")

LICENCIA = os.path.join(PATH, "../", "COPYING")

# Iconos
ICONOS = {
    "nuevo": os.path.join(PATH, "imagenes", "nuevo.png"),
    "abrir": os.path.join(PATH, "imagenes", "abrir.png"),
    "guardar": os.path.join(PATH, "imagenes", "guardar.png"),
    "guardar-como": os.path.join(PATH, "imagenes", "guardar.png"),
    "salir": os.path.join(PATH, "imagenes", "salir.png"),
    "logo": os.path.join(PATH, "imagenes", "logo.png"),
    "icono": os.path.join(PATH, "imagenes", "icono.png"),
    "print": os.path.join(PATH, "imagenes", "print.png"),
    "compilar": os.path.join(PATH, "imagenes", "compilar.png"),
    "ejecutar": os.path.join(PATH, "imagenes", "play.png"),
    "deshacer": os.path.join(PATH, "imagenes", "deshacer.png"),
    "rehacer": os.path.join(PATH, "imagenes", "rehacer.png"),
    "cortar": os.path.join(PATH, "imagenes", "cortar.png"),
    "copiar": os.path.join(PATH, "imagenes", "copiar.png"),
    "pegar": os.path.join(PATH, "imagenes", "pegar.png"),
    "buscar": os.path.join(PATH, "imagenes", "buscar.png")
    }

# Estilos de color - Editor
COLOR_EDITOR = {
    "texto": "#dfe1dd",
    "fondo": "#333333",
    "linea-actual": "#919191"
    }

# Atajos de teclas
ATAJOS = {
    "nuevo-archivo": "Ctrl+N",
    "abrir-archivo": "Ctrl+O"
    }