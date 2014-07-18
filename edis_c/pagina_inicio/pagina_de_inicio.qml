/*
* <Archivo en lenguaje QML.>
* Copyright (C) <2014>  <Gabriel Acosta>
*
* EDIS-C is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* EDIS-C is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with EDIS-C.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick 1.1

Rectangle 
{
	id: edis

	property int _padding: (central.width / 4)	
	signal nuevoArchivo
	signal abrirArchivo

	gradient: Gradient 
	{
         GradientStop 
		 { 
			position: 0.1;
			color: "#d4d4d4" 
		 }
         GradientStop 
		 { 
			position: 0.5; 
		 	color: "#232323" 
		 }
     }



	Rectangle 
	{
		id: central
		color: "white"
        anchors.fill: parent
        radius: 5
        anchors.margins: parent.height / 40
        smooth: true

		gradient: Gradient 
		{}

		Image 
		{
			id: fondo
			source: "fondo.png"
			anchors.left: parent.left
			anchors.top: parent.top
			opacity: 0.15
			fillMode: Image.PreserveAspectFit
		}

		Text 
		{
			id: saludo
			text: "¡Bienvenido a EDIS-C!"
			anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
			color: "#2e2e2e"
			font.bold: true
   	        font.pointSize: 45
 	        style: Text.Raised
 	        styleColor: "black"	
		}
		
		Image 
		{
			id: logo
			source: "seiryu.png"
			anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
			anchors.topMargin: 60	
			fillMode: Image.PreserveAspectFit
		}	

		Text 
		{
			id: descripcion
			width: 500
			font.pointSize: 13
			anchors.horizontalCenter: parent.horizontalCenter
			anchors.top: logo.bottom
			
			text: "EDIS-C es un Entorno de Desarrollo Integrado para el lenguaje C. Es Software Libre y posee herramientas útiles que le ayudaran en la programación con este lenguaje."
			wrapMode: Text.WordWrap
		}

		Column 
		{
			id: columnaB
			anchors.top: descripcion.bottom
			anchors.horizontalCenter: parent.horizontalCenter
			
			
			property int buttonWidth: 110
			Row 
			{
				spacing: 10
				Boton 
				{
					width: columnaB.buttonWidth
					height: 35
					text: "Nuevo archivo"
					onClicked: nuevoArchivo();
				}

				Boton 
				{
					width: columnaB.buttonWidth
					height: 35
					text: "Abrir archivo"
					onClicked: abrirArchivo();
				}
			}

		}

		Text 
		{
			anchors.bottom: parent.bottom
			width: 350
			height: 30
			font.italic: true
			anchors.right: parent.right
			color: "black"
			text: "EDIS-C está escrito en"
		}

		Image 
		{
			id: pyLogo
			source: "pylogo.png"
			anchors.bottom: parent.bottom
			anchors.right: parent.right
		}
	}
	
}
