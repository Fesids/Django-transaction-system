import os
from importlib import import_module

APPLICATION_ENVIRONMENT = 'local'
# APPLICATION_ENVIRONMENT = "dev"
## APPLICATION_ENVIRONMENT = "uat"

SETTINGS_BY_ENVIRONMENT = {
    'local': 'application.settings.local',
    'dev': 'application.settings.dev',
    'uat': 'application.settings.uat',
    'prod': 'application.settings.prod'
}

# TODO: get setting base on current environment

def get_django_settings():
    DJANGO_SETTINGS_MODULE = SETTINGS_BY_ENVIRONMENT.get(APPLICATION_ENVIRONMENT)
    
    if DJANGO_SETTINGS_MODULE:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', DJANGO_SETTINGS_MODULE)
        settings_module = import_module(DJANGO_SETTINGS_MODULE)
        return settings_module
    else:
        print(f"Settings not found for '{APPLICATION_ENVIRONMENT}' environment")
        

def get_setting(setting_name):
    settings_module = get_django_settings()
    
    if hasattr(settings_module, setting_name):
        return getattr(settings_module, setting_name)
    
    else:
        print(f"{setting_name} not found in the settings.")