import os
import sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

try:
    import importlib
    mod = importlib.import_module('matchapp.templatetags.admin_extras')
    print('Imported admin_extras OK — functions:', [name for name in dir(mod) if not name.startswith('_')])
except Exception as e:
    print('ERROR importing admin_extras:', type(e).__name__, e)
    raise
