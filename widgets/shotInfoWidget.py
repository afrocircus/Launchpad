__author__ = 'Nata'

from PyQt4 import QtGui


class ShotInfoWidget(QtGui.QWidget):

    def __init__(self):

        super(ShotInfoWidget, self).__init__()
        layout = QtGui.QGridLayout()
        self.setLayout(layout)

        glayout = QtGui.QGridLayout()
        layout.addLayout(glayout, 0, 0)

        glayout.addWidget(QtGui.QLabel('Episode: '), 0, 0)
        self.epLabel = QtGui.QLabel('')
        glayout.addWidget(self.epLabel, 0, 1)

        glayout.addWidget(QtGui.QLabel('Sequence: '), 1, 0)
        self.sqLabel = QtGui.QLabel('')
        glayout.addWidget(self.sqLabel, 1, 1)

        glayout.addWidget(QtGui.QLabel('Shot: '), 2, 0)
        self.shotLabel = QtGui.QLabel('')
        glayout.addWidget(self.shotLabel, 2, 1)

        glayout.addWidget(QtGui.QLabel('Task Type: '), 3, 0)
        self.taskLabel = QtGui.QLabel('')
        glayout.addWidget(self.taskLabel, 3, 1)

        glayout.addWidget(QtGui.QLabel('Priority: '), 4, 0)
        self.priorityLabel = QtGui.QLabel('')
        glayout.addWidget(self.priorityLabel, 4, 1)

        glayout.addWidget(QtGui.QLabel('Status: '), 5, 0)
        self.statusLabel = QtGui.QLabel('')
        glayout.addWidget(self.statusLabel, 5, 1)

        glayout.addWidget(QtGui.QLabel('File: '), 6, 0)
        self.fileLabel = QtGui.QLabel('No File Found')
        glayout.addWidget(self.fileLabel, 6, 1)

        glayout.addItem(QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding),7,0)

        thumbnail = QtGui.QImage('widgets/images/thumbnail.png')
        thumbnailLabel = QtGui.QLabel('')
        thumbnailLabel.setPixmap(QtGui.QPixmap(thumbnail))
        vlayout = QtGui.QVBoxLayout()
        vlayout.addWidget(thumbnailLabel)
        vlayout.addItem(QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))

        layout.addItem(QtGui.QSpacerItem(50, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum))
        layout.addLayout(vlayout, 0, 2)

    def populateShotInfo(self, infoDict):

        self.epLabel.setText(infoDict['episode'])
        self.sqLabel.setText(infoDict['sequence'])
        self.shotLabel.setText(infoDict['shot'])
        self.taskLabel.setText(infoDict['task'])
        self.priorityLabel.setText(infoDict['priority'])
        self.statusLabel.setText(infoDict['status'])
