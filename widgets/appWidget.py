__author__ = 'Nata'

from PyQt4 import QtGui
from application import ApplicationStore
from application import ApplicationLauncher

class AppWidget(QtGui.QWidget):

    identifier = 'ftrack-connect-legacy-launch-application'

    def __init__(self):

        super(AppWidget, self).__init__()

        self.applicationStore = ApplicationStore()
        self.launcher = ApplicationLauncher(self.applicationStore)

        self.discover()

    def discover(self):
        # Discover all available applications

        items = []
        applications = self.applicationStore.applications
        applications = sorted(
            applications, key=lambda application: application['label']
        )

        for application in applications:
            applicationIdentifier = application['identifier']
            label = application['label']
            items.append({
                'actionIdentifier': self.identifier,
                'label': label,
                'icon': application.get('icon', 'default'),
                'applicationIdentifier': applicationIdentifier
            })

        self.displayAppButtons(items)

    def displayAppButtons(self, items):

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        for item in items:
            button = QtGui.QPushButton(item['label'])
            button.setIcon(QtGui.QIcon(item['icon']))
            layout.addWidget(button)
            button.clicked.connect(lambda: self.launch(item))

        layout.addItem(QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))

    def launch(self, item):
        # Triggered when one of the applications is to be launched

        applicationIdentifier = item['applicationIdentifier']
        message = self.launcher.launch(applicationIdentifier)
        print message