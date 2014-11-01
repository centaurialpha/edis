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

	property int _relleno: (central.width / 4)	
    property bool comprimido: true	
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

	onWidthChanged: 
	{
        if(edis.width < 500)
		{
            comprimido = true;
            edis._relleno = (central.width / 2);
            logo.width = 300;
        }
		else
		{
            comprimido = false;
            edis._relleno = (central.width / 4);
            logo.width = logo.sourceSize.width;
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
			anchors.leftMargin: edis.comprimido ? 10 : edis.get_relleno(logo);			
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
			anchors.topMargin: edis.comprimido ? 10: edis.get_relleno(saludo);
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
			anchors.topMargin: edis.comprimido ? 10: edis.get_relleno(descripcion);
			
			text: "EDIS-C es un Entorno de Desarrollo Integrado para el lenguaje C. Es Software Libre y posee herramientas útiles que le ayudaran en la programación con este lenguaje."
			wrapMode: Text.WordWrap
		}

		Column 
		{
			id: columnaB
			anchors.top: descripcion.bottom
			anchors.horizontalCenter: parent.horizontalCenter
			anchors.topMargin: edis.comprimido ? 10: edis.get_relleno(columnaB);
			
			property int buttonWidth: comprimido ? (central.width/2) - 20 : (central.width/4) - 50
			Row 
			{
				spacing: 10
				Boton 
				{
					width: columnaB.buttonWidth
					height: 30
					text: "Nuevo archivo"
					onClicked: nuevoArchivo();
				}

				Boton 
				{
					width: columnaB.buttonWidth
					height: 30
					text: "Abrir archivo"
					onClicked: abrirArchivo();
				}
			}

		}
	}

	Row
	{
		spacing: 10
		anchors.right: parent.right
		anchors.bottom: parent.bottom
		anchors.bottomMargin: 20
		anchors.rightMargin: 30
		
		Text 
		{
			id: edis_by
			height: pyLogo.height			
			anchors.top: parent.top
			anchors.topMargin: 0		
			font.italic: true
			anchors.rightMargin: edis.get_relleno(edis_by);
			color: "black"
			styleColor: "white"
			text: "EDIS-C está escrito en"
			verticalAlignment: Text.AlignVCenter		
		}

		Image 
		{
			id: pyLogo
			source: "pylogo.png"
			
		}
	}
	function get_relleno(item)
	{
		var newrelleno = (edis._relleno - (item.width/2)) - 10;
		return newrelleno;
	}	
	
}
