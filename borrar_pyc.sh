#!/bin/bash
#===============================================================================
#
#          FILE:  borrar_pyc.sh
# 
#         USAGE:  ./borrar_pyc.sh 
# 
#   DESCRIPTION:  Elimina los archivos .pyc
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR:  gabo@alphacentauri 
#       COMPANY:  
#       VERSION:  1.0
#       CREATED:  29/05/14 01:50:43 ART
#      REVISION:  ---
#===============================================================================

find . -iname '*.pyc' -delete
