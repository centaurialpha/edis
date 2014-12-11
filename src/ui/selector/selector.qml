import QtQuick 1.1

Rectangle {
    id: contenedor
    width: 380
    height: 380
    color: "#cacaca"
    border.color: "#1c1c1c"
    radius: 2

    signal abrirArchivo(int indice)

    Rectangle {
        id: contenedorLista
        width: 350
        height: 280
        color: "#d5d5d5"
        anchors.horizontalCenter: contenedor.horizontalCenter
        y: 70
        border.color: "#000000"
        radius: 2
        clip: true

        ListView {
            id: lista
            anchors.fill: parent
            anchors.topMargin: 15
            model: modeloEjemplo

            delegate: Text {
                x: 10

                font.pointSize: 14
                text: nombre
            }
            highlight: Rectangle {
                color: "#b9b9b9"
                radius: 2
                width: lista.width - 8
                x: 4
            }

            focus: true
            clip: true

            Keys.onReturnPressed: {
                var indice = lista.currentIndex
                contenedor.abrirArchivo(indice)
            }
        }

        ListModel { id: modeloEjemplo }
    }

    Text {
        text: "Archivos abiertos"
        color: "gray"
        font.bold: true
        font.pointSize: 12
        x: 10
        y: 10

    }

    ParallelAnimation {
        id: animacion
        running: true
        NumberAnimation { target: contenedorLista; property: "width"; from: 0; to: 350; duration: 300 }
        NumberAnimation { target: contenedorLista; property: "height"; from: 0; to: 280; duration: 300 }
        }

    function cargar_archivo(nombre){
        modeloEjemplo.append({"nombre": nombre})

    }

    function item_actual(indice){
        lista.currentIndex = indice
    }
}
