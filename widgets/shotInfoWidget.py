__author__ = 'Natasha Kelkar'

from PyQt4 import QtGui


class ShotInfoWidget(QtGui.QWidget):

    def __init__(self):

        super(ShotInfoWidget, self).__init__()
        layout = QtGui.QGridLayout()
        self.setLayout(layout)

        self.glayout = QtGui.QGridLayout()
        layout.addLayout(self.glayout, 0, 0)

        thumbnail = QtGui.QImage('widgets/images/thumbnail.png')
        thumbnailLabel = QtGui.QLabel('')
        thumbnailLabel.setPixmap(QtGui.QPixmap(thumbnail))
        vlayout = QtGui.QVBoxLayout()
        vlayout.addWidget(thumbnailLabel)
        vlayout.addItem(QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))

        layout.addItem(QtGui.QSpacerItem(50, 10, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum))
        layout.addLayout(vlayout, 0, 2)

    def populateShotInfo(self, infoDict):
        i = 0
        for key in infoDict.keys():
            self.glayout.addWidget(QtGui.QLabel('%s: ' % key), i, 0)
            self.glayout.addWidget(QtGui.QLabel(infoDict[key]), i, 1)
            i = i+1
        #self.glayout.addItem(QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding),i,0)

    def clearLayout(self):
        for i in reversed(range(self.glayout.count())):
            self.glayout.itemAt(i).widget().deleteLater()
