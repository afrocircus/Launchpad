__author__ = 'Nata'

from PyQt4 import QtGui


class TaskWidget(QtGui.QListWidget):

    def __init__(self):
        super(TaskWidget, self).__init__()
        self.setFrameShape(0)

    def addTask(self, taskList):
        self.addItems(taskList)

    def removeAllTasks(self):
        self.clear()
