import QtQuick 6.0
import QtQuick.Controls 6.0
import QtQuick.Layouts 6.0
import Qt5Compat.GraphicalEffects

ApplicationWindow {
    id: root
    title: "Grammar Interpreter"
    width: 1200
    height: 700
    visible: true
    color: "#2D2D30"

    readonly property color accentColor: "#4EC9B0"
    readonly property color panelColor: "#252526"
    readonly property color dividerColor: "#3E3E42"
    readonly property color textColor: "#D4D4D4"

    SplitView {
        anchors.fill: parent
        handle: Rectangle {
            implicitWidth: 8
            color: dividerColor
        }

        ColumnLayout {
            Layout.minimumWidth: 400
            spacing: 15

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 150
                color: panelColor
                radius: 8
                layer.enabled: true
                layer.effect: DropShadow {
                    radius: 12
                    samples: 24
                    color: "#80000000"
                }

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 15
                    spacing: 10

                    Label {
                        text: "Symbols"
                        color: accentColor
                        font.bold: true
                        font.pixelSize: 16
                    }

                    GridLayout {
                        columns: 2
                        columnSpacing: 15
                        rowSpacing: 10
                        
                        Label { 
                            text: "Terminals:" 
                            color: textColor
                        }
                        
                        Text {
                            text: bridge.terminals.join(", ")
                            color: textColor
                            Layout.fillWidth: true
                            elide: Text.ElideRight
                        }
                        
                        Label { 
                            text: "Non-terminals:" 
                            color: textColor
                        }
                        
                        Text {
                            text: bridge.non_terminals.join(", ")
                            color: textColor
                            Layout.fillWidth: true
                            elide: Text.ElideRight
                        }
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: panelColor
                radius: 8
                layer.enabled: true
                layer.effect: DropShadow {
                    radius: 12
                    samples: 24
                    color: "#80000000"
                }

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 15
                    spacing: 10

                    Label {
                        text: "Grammar Rules"
                        color: accentColor
                        font.bold: true
                        font.pixelSize: 16
                    }

                    ListView {
                        id: rulesList
                        model: bridge.rules
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        clip: true
                        spacing: 8

                        delegate: Rectangle {
                            width: rulesList.width
                            height: 40
                            color: "transparent"

                            RowLayout {
                                anchors.fill: parent
                                spacing: 10
                                
                                Text {
                                    text: modelData.lhs
                                    color: textColor
                                    Layout.preferredWidth: 150
                                    elide: Text.ElideRight
                                }
                                
                                Rectangle {
                                    width: 30
                                    height: 2
                                    color: dividerColor
                                    rotation: 90
                                    Layout.alignment: Qt.AlignVCenter
                                }
                                
                                Text {
                                    text: modelData.rhs
                                    color: "#FFFFFF"
                                    Layout.fillWidth: true
                                    elide: Text.ElideRight
                                }
                            }

                            Rectangle {
                                anchors.bottom: parent.bottom
                                width: parent.width
                                height: 1
                                color: dividerColor
                            }
                        }
                    }
                }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            spacing: 15

            RowLayout {
                spacing: 15
                
                TextField {
                    id: inputField
                    placeholderText: "Enter input string..."
                    Layout.fillWidth: true
                    color: textColor
                    background: Rectangle {
                        color: panelColor
                        radius: 5
                    }
                }
                
                Button {
                    text: "Start"
                    background: Rectangle {
                        color: accentColor
                        radius: 5
                    }
                    contentItem: Text {
                        text: parent.text
                        color: "#FFFFFF"
                        horizontalAlignment: Text.AlignHCenter
                    }
                    onClicked: bridge.process_input(inputField.text)
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: panelColor
                radius: 8
                layer.enabled: true
                layer.effect: DropShadow {
                    radius: 12
                    samples: 24
                    color: "#80000000"
                }

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 15
                    spacing: 10

                    Label {
                        text: "Execution Steps"
                        color: accentColor
                        font.bold: true
                        font.pixelSize: 16
                    }

                    ListView {
                        model: bridge.steps
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        clip: true
                        spacing: 5

                        delegate: Text {
                            text: modelData
                            width: parent.width
                            color: textColor
                            wrapMode: Text.Wrap
                            padding: 5
                        }

                        ScrollBar.vertical: ScrollBar {
                            policy: ScrollBar.AsNeeded
                            contentItem: Rectangle {
                                implicitWidth: 6
                                radius: 3
                                color: accentColor
                            }
                        }
                    }
                }
            }
        }
    }
}
