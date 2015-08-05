__author__ = 'Nata'

import os
import lucidity

templatesPath = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'templates')
    )
templates = lucidity.discover_templates(paths=[templatesPath])

data = {
    'project': {
        'name': 'launcher'
    },
    'shot': {
        'name': 'shot 001'
    }
}

for template in templates:
    print template.format(data)
