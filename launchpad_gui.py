__author__ = 'Nata'

import sys

from PyQt4 import QtGui, QtCore
from widgets.taskWidget import TaskWidget
from launchpad import LaunchPad
from widgets.shotInfoWidget import ShotInfoWidget
from widgets.appWidget import AppWidget
from style import pyqt_style_rc


class LaunchPadGui(QtGui.QMainWindow):

    def __init__(self):
        super(LaunchPadGui, self).__init__()
        self.setWindowTitle('LocoVFX Launchpad')
        window = QtGui.QWidget()
        self.setWindowIcon(QtGui.QIcon('widgets/images/loco_icon.png'))

        f = QtCore.QFile('style/style.qss')
        f.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        ts = QtCore.QTextStream(f)
        self.stylesheet = ts.readAll()
        window.setStyleSheet(self.stylesheet)

        self.centralLayout = QtGui.QGridLayout()
        window.setLayout(self.centralLayout)
        self.setCentralWidget(window)
        self.launcher = LaunchPad()
        self.username = self.launcher.getUsername()

        self.setupUI()

    def setupUI(self):

        usernameLabel = QtGui.QLabel('Username: %s' % self.username)
        self.centralLayout.addWidget(usernameLabel, 0, 2)

        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(QtGui.QLabel('Project:'))
        projComboBox = QtGui.QComboBox()
        projComboBox.setFixedSize(100,20)
        projComboBox.addItems(self.launcher.getProjects())
        projComboBox.currentIndexChanged[str].connect(self.populateTasks)
        hlayout.addWidget(projComboBox)
        hlayout.addItem(QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum))
        self.centralLayout.addLayout(hlayout, 0, 0)

        taskGroupBox = QtGui.QGroupBox('My Tasks')
        self.shotGroupBox = QtGui.QGroupBox('Shot Information')
        self.appGroupBox = QtGui.QGroupBox('Available Apps')
        self.centralLayout.addWidget(taskGroupBox, 1, 0)
        self.centralLayout.addWidget(self.shotGroupBox, 1, 1)
        self.centralLayout.addWidget(self.appGroupBox, 1, 2)

        self.taskWidget = TaskWidget()
        taskGroupLayout = QtGui.QGridLayout()
        taskGroupBox.setLayout(taskGroupLayout)
        taskGroupLayout.addWidget(self.taskWidget)
        self.taskWidget.itemClicked.connect(self.taskItemClicked)
        self.taskWidget.setMinimumSize(350,200)
        self.populateTasks(projComboBox.currentText())

        self.shotInfoWidget = ShotInfoWidget()
        shotGroupLayout = QtGui.QGridLayout()
        self.shotGroupBox.setLayout(shotGroupLayout)
        shotGroupLayout.addWidget(self.shotInfoWidget)
        self.shotGroupBox.setVisible(False)

        self.appWidget = AppWidget()
        appGroupLayout = QtGui.QGridLayout()
        self.appGroupBox.setLayout(appGroupLayout)
        appGroupLayout.addWidget(self.appWidget)
        self.appGroupBox.setVisible(False)

    def populateTasks(self, selection):

        self.taskWidget.clear()
        self.tasks = self.launcher.getUserTasks(self.username, selection)
        taskList = [ task['taskName'] for task in self.tasks ]
        self.taskWidget.addTask(taskList)

    def taskItemClicked(self, item):

        taskName = str(item.text())
        taskNameList = taskName.split('/')
        infoDict = {}
        infoDict['episode'] = taskNameList[0]
        infoDict['sequence'] = taskNameList[1]
        infoDict['shot'] = taskNameList[2]
        infoDict['task'] = taskNameList[3]

        for task in self.tasks:
            if task['taskName'] == taskName:
                infoDict['priority'] = task['priority']
                infoDict['status'] = task['status']
                break

        self.shotGroupBox.setVisible(True)
        self.shotInfoWidget.populateShotInfo(infoDict)
        self.appGroupBox.setVisible(True)


def main():
    app = QtGui.QApplication(sys.argv)
    gui = LaunchPadGui()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
