"""
WSGI config for sarscov2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys
import site
from django.core.wsgi import get_wsgi_application

python_home = '/ssd/Howard/vaccine_env'
#activate_this = python_home + '/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))

# Calculate path to site-packages directory.

python_version = '.'.join(map(str, sys.version_info[:2]))
site_packages = python_home + '/lib/python%s/site-packages' % python_version
site.addsitedir(site_packages)

# Remember original sys.path.

prev_sys_path = list(sys.path)

# Add the site-packages directory.

site.addsitedir(site_packages)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vaccine-cost-model.settings')

sys.path.append('/ssd/Howard/vaccine-cost-model/')
sys.path.append('/ssd/Howard/vaccine-cost-model/vaccine-cost-model/')

application = get_wsgi_application()
