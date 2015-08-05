__author__ = 'Natasha Kelkar'

import os
import ftrack
import lucidity
import errno


class LaunchPad(object):

    def __init__(self):
        super(LaunchPad, self).__init__()

        self.prefix = 'C:/Users/Nata/Documents/Loco'

        templatesPath = os.path.abspath( os.path.join(os.path.dirname(__file__), 'templates'))
        self.templates = lucidity.discover_templates(paths=[templatesPath])

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
                taskDict['parentType'] = task.getParent().getType().getName()
                taskDict['path'] = self.buildTemplateData(taskDict,proj)
                #self.makeDirs(taskDict['path'])
            taskList.append(taskDict)
        return taskList

    def buildTemplateData(self, task, project):
        data = {}
        data['project'] = project
        taskNameList = task['taskName'].split('/')
        if taskNameList[0] == 'Asset builds':
            data['asset'] = taskNameList[1]
            if task['parentType'] == 'Character':
                template = self.getTemplate('lib-char-dir')
            else:
                template = self.getTemplate('lib-envir-dir')
        else:
            data['episode'] = taskNameList[0]
            data['sequence'] = taskNameList[1]
            data['shot'] = taskNameList[2]
            template = self.getTemplate('shot-dir')
        try:
            templatePath = template.format(data)
        except lucidity.error.FormatError:
            print('Not enough information provided for this template.')

        # Raise error if path is absolute since it will not be joined
        # with prefix correctly.
        if os.path.isabs(templatePath):
            raise ValueError('Template path should be relative.')
        fullpath = os.path.join(self.prefix, templatePath)

        return fullpath

    def makeDirs(self, templatePath):

        try:
            os.makedirs(templatePath)
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise

    def getTemplate(self, name):
        for template in self.templates:
            if template.name == name:
                return template

