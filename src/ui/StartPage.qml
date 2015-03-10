import QtQuick 1.1

Rectangle {
    id: root

    gradient: Gradient {
         GradientStop { position: 0.0; color: "#333333" }
         GradientStop { position: 1.0; color: "#666666" }
     }

    Image { source: "../images/sources/logo.png"; anchors.horizontalCenter: root.horizontalCenter }

    Text {
        text: qsTr("Copyright © 2014-" + Qt.formatDate(new Date(), "yyyy ") + "Edis under GPLv3+ License")
        font.pointSize: 10
        color: "#FFFFFF"
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.bottomMargin: 5
        anchors.rightMargin: 10
    }

    Text {
        id: link
        text: qsTr("<b>Edis</b> is Free Software! <a href='http://centaurialpha.github.io/edis'><span style='color: lightblue;'>http://centaurialpha.github.io/edis</span></a>")
        font.pointSize: 10
        color: "#FFFFFF"
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.bottomMargin: 5
        anchors.leftMargin: 10

        onLinkActivated: Qt.openUrlExternally(link)

    }

}
