import QtQuick 1.1

Rectangle {
    id: root

    color: "#292e30"
    property int duracion: 800;

    ParallelAnimation {
        id: animacion
        running: false

        NumberAnimation { target: mensaje; property: "opacity"; to: 1; from: 0; duration: root.duracion }
    }

    Column {
        anchors.verticalCenter: root.verticalCenter;
        anchors.horizontalCenter: root.horizontalCenter;
        anchors.top: root.top;
        anchors.topMargin: 30;
        spacing: 150;

        Image { source: "../images/sources/logo.png"; anchors.horizontalCenter: parent.horizontalCenter }

        Text {
            id: mensaje

            color: "#343b3d";
            font.bold: true;
            font.pointSize: 32;
        }
    }

    Text {
        text: qsTr("Copyright © 2014-" + Qt.formatDate(new Date(), "yyyy ") + "Edis under GPLv3+ License")
        font.pointSize: 10
        color: "#BABDB6"
        style: Text.Raised;
        anchors.bottom: root.bottom
        anchors.left: root.left
        anchors.bottomMargin: 5
        anchors.leftMargin: 10
    }

    Row {
        anchors.bottomMargin: 5
        anchors.rightMargin: 10
        anchors.bottom: parent.bottom
        anchors.right: parent.right

        Text {
            text: qsTr("Powered by: ");
            color: "#BABDB6";
            style: Text.Raised;
            height: logo.height;
            verticalAlignment: Text.AlignVCenter;
        }

        Image { id: logo; source: "../images/sources/python-logo.png"; }
        Image { source: "../images/sources/qt-logo.png"; }
    }

    function show_text(texto) {
        animacion.start();
        mensaje.text = texto;
    }
}
