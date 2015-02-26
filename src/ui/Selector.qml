import QtQuick 1.1

Rectangle {
    id: root

    width: 380; height: 260;
    color: "#474641"

    signal openFile(int index)
    signal animationCompleted()

    ListView {
        id: list

        clip: true
        model: ListModel{ id:model }
        anchors.fill: parent
        anchors.topMargin: 15
        anchors.leftMargin: 30
        delegate: Text { color: "#dedede"; text: filename; font.pointSize: 14 }
        highlight: Rectangle { color: "gray"; opacity: 0.2 }
        focus: true

        Keys.onReturnPressed: {
            var index = list.currentIndex
            root.openFile(index)
        }
    }

    ParallelAnimation {
        id: animation

        running: false
        NumberAnimation { target: root; property: "x"; to: 0; from: 200; duration: 300 }
        NumberAnimation { target: root; property: "y"; to: 0; from: 200; duration: 300 }
        NumberAnimation { target: root; property: "height"; to: 260; duration: 300 }
        NumberAnimation { target: root; property: "width"; to: 380; duration: 300 }

    }

    ParallelAnimation {
        id: closeAnimation

        running: false
        NumberAnimation { target: root; property: "x"; to: 200; duration: 300 }
        NumberAnimation { target: root; property: "y"; to: 200; duration: 300 }
        NumberAnimation { target: root; property: "height"; to: 0; duration: 300 }
        NumberAnimation { target: root; property: "width"; to: 0; duration: 300 }

        onCompleted: {
            root.visible = false;
            root.animationCompleted();
        }

    }

    function load_file(filename){
        model.append({"filename": filename})
    }

    function current_index(index){
        list.currentIndex = index
    }

    function start_animation(){
        animation.start()
    }

    function close_widget(){
        closeAnimation.start()
    }
}

