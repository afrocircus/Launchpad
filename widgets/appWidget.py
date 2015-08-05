__author__ = 'Natasha Kelkar'

import os
from PyQt4 import QtGui
from application import ApplicationStore
from application import ApplicationLauncher

class AppWidget(QtGui.QWidget):

    identifier = 'ftrack-connect-legacy-launch-application'

    def __init__(self):

        super(AppWidget, self).__init__()

        self.applicationStore = ApplicationStore()
        self.launcher = ApplicationLauncher(self.applicationStore)

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addItem(QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding), 6, 0)

        #self.discover()

    def discover(self, filename):
        # Discover all available applications

        items = []
        applications = self.applicationStore.applications
        applications = sorted(
            applications, key=lambda application: application['label']
        )

        for application in applications:
            applicationIdentifier = application['identifier']
            label = application['label']
            if filename == '' or filename.split('.')[-1] in application['fileType']:
                items.append({
                    'actionIdentifier': self.identifier,
                    'label': label,
                    'icon': application.get('icon', 'default'),
                    'applicationIdentifier': applicationIdentifier,
                    'file': filename
                })

        self.displayAppButtons(items)

    def displayAppButtons(self, items):

        self.clearAppButtons()
        i = 0
        for item in items:
            button = QtGui.QPushButton(item['label'])
            button.setIcon(QtGui.QIcon(item['icon']))
            self.layout.addWidget(button, i, 0)
            i = i + 1
            button.clicked.connect(lambda: self.launch(item))

    def clearAppButtons(self):
        for i in reversed(range(self.layout.count())):
            if not isinstance(self.layout.itemAt(i), QtGui.QSpacerItem):
                self.layout.itemAt(i).widget().deleteLater()

    def launch(self, item):
        # Triggered when one of the applications is to be launched

        filepath = self.getFilename(item['label'])
        filepath = str(filepath).replace('/', '\\')
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        applicationIdentifier = item['applicationIdentifier']
        if item['file'] == '':
            launchArgumets = ['-proj', filepath]
        else:
            launchArgumets = ['-file', item['file'], '-proj', filepath]
        message = self.launcher.launch(applicationIdentifier, launchArgumets)
        #print message

    def getFilename(self, label):
        path = os.path.join(self.projectDir, label.split()[0].lower())
        return path