import QtQuick 1.1

Rectangle {
    id: root

    gradient: Gradient {
         GradientStop { position: 0.0; color: "#41403b" }
         GradientStop { position: 1.0; color: "#5a584f" }
     }

    Rectangle {
        id: main

        color: "#5a584f"
        anchors.fill: root
        anchors.margins: 15
        radius: 5

        Column {
            id: mainLayout

            spacing: 10
            anchors.horizontalCenter: parent.horizontalCenter

            Row {
                spacing: 30

                Image {
                    id: logo
                    source: "../../src/images/icon.png"
                }

                Column {
                    Text { text: qsTr("EDIS"); color: "#dedede"; font.pointSize: 30 }
                    Text { text: qsTr("a simple cross-platform IDE for C"); color: "#dedede" }
                }
            }
        }

    }

    Text {
        text: qsTr("Copyright © 2014-2015 Edis under GPLv3 License")
        font.pointSize: 10
        color: "#dedede"
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.bottomMargin: 5
        anchors.rightMargin: 10
    }

    Text {
        id: link
        text: qsTr("Edis use the <b>Clang</b> compiler: <a href='http://clang.llvm.org'><span style='color: #ffffff;'>http://clang.llvm.org</span></a>")
        font.pointSize: 10
        color: "#dedede"
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.bottomMargin: 5
        anchors.leftMargin: 10

        onLinkActivated: Qt.openUrlExternally(link)

    }
}
