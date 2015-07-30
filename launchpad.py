__author__ = 'Nata'

import os
import ftrack

class LaunchPad(object):

    def __init__(self):
        super(LaunchPad, self).__init__()

    def getUsername(self):
        # This will be read from a config file. Hardcoding it here temporarily
        username = 'natasha.kelkar@gmail.com'
        os.environ['USERNAME'] = username
        return username

    def getProjects(self):
        projects = ftrack.getProjects()
        projectList = [ project.getName() for project in projects ]
        return projectList

    def getUserTasks(self, username, project):

        user = ftrack.getUser(username)
        tasks = user.getTasks()
        taskList = []
        for task in tasks:
            taskDict = {}
            proj = task.getProject().getName()
            if proj == project:
                parents = task.getParents()
                taskName = task.getName()
                for count in xrange(0, len(parents)-1):
                    taskName = '%s/%s' % (parents[count].getName(), taskName)
                taskDict['taskName'] = taskName
                taskDict['priority'] = task.getPriority().getName()
                taskDict['taskID'] = task.getId()
                taskDict['status'] = task.getStatus().getName()
            taskList.append(taskDict)
        return taskList

