#!/bin/bash

# Script para convertir archivos .qrc a .py

pyrcc4 -py3 src/resources.qrc -o src/resources.py
