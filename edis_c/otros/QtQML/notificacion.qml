import QtQuick 1.1

Rectangle
{
    id: rectangulo
    width: 400
    height: 40
    color: "black"
    opacity: 0
    radius: 0
    border.color: "#3c64c8"
    border.width: 3
    property int interval: 3000
    signal close

    function setText(message)
    {
        areaTexto.text = message;
    }

    function setColor(background_color, foreground_color)
    {
        rectangulo.color = background_color;
        areaTexto.color = foreground_color;
    }

    function start(interval)
    {
        rectangulo.interval = interval;
        mostrarRectangulo.start();
    }

    SequentialAnimation
    {
        id: mostrarRectangulo
        running: false
        NumberAnimation
        {
            target: rectangulo;
            property: "opacity";
            to: 1;
            duration: (rectangulo.interval / 2);
            easing.type: Easing.InOutQuad
        }
        NumberAnimation
        {
            target: rectangulo;
            property: "opacity";
            to: 0;
            duration: (rectangulo.interval / 2);
            easing.type: Easing.InOutQuad
        }
    }

    onOpacityChanged:
    {
        if(rectangulo.opacity == 0)
        {
            rectangulo.close();
        }
    }

    Text
    {
        id: areaTexto
        text: ""
        wrapMode: Text.WordWrap
        font.pixelSize: 16
        font.bold: true
        anchors.fill: parent
        anchors.margins: 5
        color: "white"
        width: rectangulo.width
        elide: Text.ElideRight
    }

    MouseArea
    {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
    }

    states: [
         State
        {
             name: "entered";
             when: mouseArea.containsMouse
             PropertyChanges
            {
                target: rectangulo;
                opacity: 1
            }
         },
         State
        {
             name: "";
             when: !mouseArea.containsMouse
             PropertyChanges { target: rectangulo; opacity: 0.5 }
         }
     ]

    transitions: Transition
    {
        reversible: true
        from: ""
        to: "entered"
        NumberAnimation
        {
            target: parent;
            properties: "opacity";
            duration: 700
        }
    }

}
