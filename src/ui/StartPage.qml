import QtQuick 1.1

Rectangle {
    id: root

    color: "#171814"

    ParallelAnimation {
        id: animation
        running: false

        NumberAnimation { target: showText; property: "opacity"; to: 1; duration: 400 }
        NumberAnimation { target: showText; property: "x"; to: 0; from: -root.width; duration: 400 }
    }

    Column {
        anchors.verticalCenter: root.verticalCenter;
        anchors.horizontalCenter: root.horizontalCenter;
        anchors.top: root.top;
        anchors.topMargin: 30;
        spacing: 150;

        Image { source: "../images/sources/logo.png"; anchors.horizontalCenter: parent.horizontalCenter }

        Text {
            id: showText

            color: "#20211c";
            font.bold: true;
            font.pointSize: 32;
        }
    }

    Text {
        text: qsTr("Copyright © 2014-" + Qt.formatDate(new Date(), "yyyy ") + "Edis under GPLv3+ License")
        font.pointSize: 10
        color: "#FFFFFF"
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
            color: "white";
            style: Text.Raised;
            height: logo.height;
            verticalAlignment: Text.AlignVCenter;
        }

        Image { id: logo; source: "../images/sources/python-logo.png"; }
        Image { source: "../images/sources/qt-logo.png"; }
    }

    function show_text(text) {
        animation.start();
        showText.text = text;
    }
}
