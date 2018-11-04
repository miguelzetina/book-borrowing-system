from importlib import import_module

from django.conf import settings


def autodiscover():
    """
    Perform an autodiscover of an api.py file in the installed apps to
    generate the routes of the registered viewsets.
    """
    for app in settings.INSTALLED_APPS:
        try:
            import_module('.'.join((app, 'api')))
        except ImportError:
            pass
