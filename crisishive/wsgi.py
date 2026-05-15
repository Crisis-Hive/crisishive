"""
WSGI config for crisishive project.
"""

import os
import sys
import traceback

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crisishive.settings')

try:
    application = get_wsgi_application()
except Exception:
    # This will print the EXACT error to the Railway logs if the app fails to start
    print("CRITICAL: Django application failed to initialize!")
    traceback.print_exc()
    sys.exit(1)
