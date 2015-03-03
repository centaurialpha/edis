import QtQuick 1.1

Rectangle {
    id: root

    width: 380; height: 260;
    color: "#474641"
    border.color: "gray";
    border.width: 2;

    signal openFile(int index)
    signal animationCompleted()
    signal close

    ListView {
        id: list

        clip: true
        model: ListModel{ id:model }
        anchors.fill: parent
        anchors.topMargin: 15
        anchors.leftMargin: 30
        delegate: Text { color: "#dedede"; text: filename; font.pointSize: 14 }
        highlight: Rectangle { color: "gray"; opacity: 0.2; width: 300 }
        focus: true

        Keys.onReturnPressed: {
            var index = list.currentIndex
            root.openFile(index)
        }

        Keys.onEscapePressed: {
            closeAnimation.start();
        }
    }

    SequentialAnimation {
        id: animation
        running: false

        NumberAnimation { target: root; property: "opacity"; to: 1; from: 0; duration: 200; easing.type: Easing.InOutQuad }

    }

    SequentialAnimation {
        id: closeAnimation
        running: false

        NumberAnimation { target: root; property: "opacity"; to: 0; from: 1; duration: 200; easing.type: Easing.InOutQuad }

    }

    onOpacityChanged: {
        if(root.opacity == 0){
            root.close();
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

