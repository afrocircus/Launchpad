
import sys
import os
import re
import logging
import subprocess


DEFAULT_VERSION_EXPRESSION = re.compile(
    r'(?P<version>\d[\d.vabc]*?)[^\d]*$'
)


class ApplicationStore(object):

    def __init__(self):
        # Instantiate store and discover applications.
        super(ApplicationStore, self).__init__()

        self.logger = logging.getLogger(
            __name__ + '.' + self.__class__.__name__
        )

        # Discover applications and store.
        self.applications = self._discoverApplications()

    def getApplication(self, identifier):
        '''
        Return first application with matching *identifier*.

        :param identifier: may contain a wildcard at the end to match the first
        substring matching entry.
        :return: None if no application matches.
        '''

        hasWildcard = identifier[-1] == '*'
        if hasWildcard:
            identifier = identifier[:-1]

        for application in self.applications:
            if hasWildcard:
                if application['identifier'].startswith(identifier):
                    return application
            else:
                if application['identifier'] == identifier:
                    return application

        return None

    def _discoverApplications(self):
        '''
        Return a list of applications that can be launched from this host.

        An application should be of the form:

            dict(
                'identifier': 'name_version',
                'label': 'Name version',
                'path': 'Absolute path to the file',
                'version': 'Version of the application',
                'icon': 'URL or name of predefined icon'
        '''

        applications = []

        if sys.platform == 'darwin':
            prefix = ['/', 'Applications']

        elif sys.platform == 'win32':
            prefix = ['C:\\', 'Program Files.*']

            applications.extend(self._searchFilesystem(
                expression=prefix + ['Autodesk', 'Maya.+', 'bin', 'maya.exe'],
                label='Maya {version}',
                applicationIdentifier='maya_{version}',
                icon='widgets/images/maya_icon.png',
                fileType= ['ma', 'mb']
            ))

            applications.extend(self._searchFilesystem(
                expression=prefix + ['Hiero\d.+', 'hiero.exe'],
                label='Hiero {version}',
                applicationIdentifier='hiero_{version}',
                icon='widgets/images/hiero_icon.png',
                fileType= ['ma', 'mb']
            ))

        return applications

    def _searchFilesystem(self, expression, label, applicationIdentifier,
                          versionExpression=None, icon=None,
                          launchArguments=None, fileType=None):
        '''
        Return list of applications found in filesystem matching *expression*.

        :param expression: should be a list of regular expressions to match against
        path segments up to the executable. Each path segment traversed will be
        matched against the corresponding expression part. The first expression
        part must not contain any regular expression syntax and must match
        directly to a path existing on disk as it will form the root of the
        search. Example::

            ['C:\\', 'Program Files.*', 'Company', 'Product\d+', 'product.exe']

        :param label: is the label the application will be given. *label* should be on
        the format "Name of app {version}".

        :param applicationIdentifier: should be on the form
        "application_name_{version}" where version is the first match in the
        regexp.

        :param versionExpression: is a regular expression used to find the version of
        the application. It will be applied against the full matching path of
        any discovered executable. It must include a named 'version' group
        which can be used in the label and applicationIdentifier templates.

        For example::

            '(?P<version>[\d]{4})'

        If not specified, then :py:data:`DEFAULT_VERSION_EXPRESSION` will be
        used.

        :param icon:

        :param launchArguments: may be specified as a list of arguments that should
        used when launching the application.
        :return: applications
        '''

        applications = []

        if versionExpression is None:
            versionExpression = DEFAULT_VERSION_EXPRESSION
        else:
            versionExpression = re.compile(versionExpression)

        pieces = expression[:]
        start = pieces.pop(0)
        if sys.platform == 'win32':
            # On Windows C: means current directory so convert roots that look
            # like drive letters to the C:\ format.
            if start and start[-1] == ':':
                start += '\\'

        if not os.path.exists(start):
            raise ValueError(
                'First part "{0}" of expression "{1}" must match exactly to an '
                'existing entry on the filesystem.'
                .format(start, expression)
            )

        expressions = map(re.compile, pieces)
        expressionsCount = len(expressions)

        for location, folders, files in os.walk(start, topdown=True):
            level = location.rstrip(os.path.sep).count(os.path.sep)
            expression = expressions[level]

            if level < (expressionsCount - 1):
                # If not yet at final piece then just prune directories.
                folders[:] = [folder for folder in folders
                              if expression.match(folder)]
            else:
                # Match executable. Note that on OSX executable might equate to
                # a folder (.app).
                for entry in folders + files:
                    match = expression.match(entry)
                    if match:
                        # Extract version from full matching path.
                        path = os.path.join(start, location, entry)

                        versionMatch = versionExpression.search(path)
                        if versionMatch:
                            version = versionMatch.group('version')
                            applications.append({
                                'identifier': applicationIdentifier.format(
                                    version=version
                                ),
                                'path': path,
                                'launchArguments': launchArguments,
                                'version': version,
                                'label': label.format(version=version),
                                'icon': icon,
                                'fileType': fileType
                            })
                        else:
                            self.logger.debug(
                                'Discovered application executable, but it '
                                'does not appear to o contain required version '
                                'information: {0}'.format(path)
                            )

                # Don't descend any further as out of patterns to match.
                del folders[:]

        return applications


class ApplicationLauncher(object):
    '''Launch applications described by an application store.

    Launched applications are started detached so exiting current process will
    not close launched applications.

    '''

    def __init__(self, applicationStore):
        '''Instantiate launcher with *applicationStore* of applications.

        *applicationStore* should be an instance of :class:`ApplicationStore`
        holding information about applications that can be launched.

        '''
        super(ApplicationLauncher, self).__init__()
        self.logger = logging.getLogger(
            __name__ + '.' + self.__class__.__name__
        )

        self.applicationStore = applicationStore

    def launch(self, applicationIdentifier, launchArguments):
        '''Launch application matching *applicationIdentifier*.

        *context* should provide information that can guide how to launch the
        application.

        Return a dictionary of information containing:

            success - A boolean value indicating whether application launched
                      successfully or not.
            message - Any additional information (such as a failure message).

        '''
        # Look up application.
        applicationIdentifierPattern = applicationIdentifier
        if applicationIdentifierPattern == 'hieroplayer':
            applicationIdentifierPattern += '*'

        application = self.applicationStore.getApplication(
            applicationIdentifierPattern
        )
        application['launchArguments'] = launchArguments

        if application is None:
            return {
                'success': False,
                'message': (
                    '{0} application not found.'
                    .format(applicationIdentifier)
                )
            }

        # Construct command.
        command = self._getApplicationLaunchCommand(application)
        print command

        success = True
        message = '{0} application started.'.format(application['label'])

        try:
            options = dict(
                close_fds=True
            )

            # Ensure that current working directory is set to the root of the
            # application being launched to avoid issues with applications
            # locating shared libraries etc.
            applicationRootPath = os.path.dirname(application['path'])
            options['cwd'] = applicationRootPath

            # Ensure subprocess is detached so closing connect will not also
            # close launched applications.
            if sys.platform == 'win32':
                options['creationflags'] = subprocess.CREATE_NEW_CONSOLE
            else:
                options['preexec_fn'] = os.setsid

            self.logger.debug(
                'Launching {0} with options {1}'.format(command, options)
            )

            process = subprocess.Popen(command, **options)

        except (OSError, TypeError):
            self.logger.exception(
                '{0} application could not be started with command "{1}".'
                .format(applicationIdentifier, command)
            )

            success = False
            message = '{0} application could not be started.'.format(
                application['label']
            )

        else:
            self.logger.debug(
                '{0} application started. (pid={1})'.format(
                    applicationIdentifier, process.pid
                )
            )

        return {
            'success': success,
            'message': message
        }

    def _getApplicationLaunchCommand(self, application):
        '''Return *application* command based on OS and *context*.

        *application* should be a mapping describing the application, as in the
        :class:`ApplicationStore`.

        *context* should provide additional information about how the
        application should be launched.

        '''
        command = None

        if sys.platform in ('win32', 'linux2'):
            command = [application['path']]

        elif sys.platform == 'darwin':
            command = ['open', application['path']]

        else:
            self.logger.warning(
                'Unable to find launch command for {0} on this platform.'
                .format(application['identifier'])
            )

        # Add any extra launch arguments if specified.
        launchArguments = application.get('launchArguments')
        if launchArguments:
            command.extend(launchArguments)

        return command

