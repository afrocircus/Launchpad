__author__ = 'Natasha Kelkar'

from lucidity import Template


def register():
    # Register templates.

    return [
        Template('proj-dir', '{project}'),
        Template('general-dir', '{project}/general'),
        Template('lib-dir', '{project}/lib'),
        Template('episode-dir', '{project}/general/{episode}'),
        Template('sequence-dir', '{project}/general/{episode}/{sequence}'),
        Template('shot-dir', '{project}/general/{episode}/{sequence}/{shot}'),
        Template('shot-maya-dir', '{project}/general/{episode}/{sequence}/{shot}/maya'),
        Template('lib-asset-dir', '{project}/lib/asset'),
        Template('lib-char-dir', '{project}/lib/asset/char/{asset}'),
        Template('lib-char-maya-dir', '{project}/lib/asset/char/{asset}/maya'),
        Template('lib-envir-dir', '{project}/lib/asset/envir/{asset}'),
        Template('lib-envir-maya-dir', '{project}/lib/asset/envir/{asset}/maya')
    ]
