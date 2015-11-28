import QtQuick 2.0
import Sailfish.Silica 1.0
import "../components"

ToggleItem {
    id: root
    anchors.fill: parent

    name: qsTr("Screenshot")
    icon: "image://theme/icon-m-device-download"
    disabled: Screenshot.busy

    onClicked: {
        window.hideWithCare()
        Screenshot.save(800)
    }
}
