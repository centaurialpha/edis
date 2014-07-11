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

	id: boton
	property alias text: txtButton.text
	signal clicked

	radius: 10
	border.color: "gray"
	border.width: 2
	
	gradient: Gradient 
	{
         GradientStop 
		 {  
			id: stop1; 
			position: 0.0; 
			color: "#232323" 
		 }
	
         GradientStop 
     	 { 
			id: stop2; 
			position: 1.0; 
			color: "#d4d4d4" 
		 }
     }

	Text 
	{
        id: txtButton
        anchors.centerIn: parent

        text: boton.text
        color: "white"
    }

	states: [
        State 
		{
            name: "ENTERED"
            PropertyChanges 
			{ 
				target: stop1; 
				color: "blue" 
			}
        },
        State 
		{
            name: "EXITED"
            PropertyChanges 
			{ 
				target: stop1; 
				color: "#232323" 
			}
        },
        State 
		{
            name: "PRESSED"
            PropertyChanges 
			{ 
				target: stop2; 
				color: "#2c59bd" 
			}

            PropertyChanges 
			{ 
				target: stop1; 
				color: "#2c59bd" 
			}
        },
        State 
		{
            name: "RELEASED"
            PropertyChanges 
			{ 
				target: stop1; 
				color: "#232323" 
			}

            PropertyChanges 
			{ 
				target: stop2; 
				color: "#d4d4d4" 
			}
        }
     ]

    MouseArea 
	{
        anchors.fill: parent
        hoverEnabled: true

        onEntered: boton.state = "ENTERED";
        onExited: boton.state = "EXITED";
        onClicked: boton.clicked();
        onPressed: boton.state = "PRESSED";
        onReleased: boton.state = "RELEASED";
    }
}
