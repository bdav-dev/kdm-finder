import os
import shelve

from models.settings_models import Settings
from util.file_system_util import get_app_root_path

SETTINGS_FILENAME = "app_settings"
SETTINGS_SHELVE_KEY = "settings"
SETTINGS_FILE_LOCATION = os.path.join(get_app_root_path(), SETTINGS_FILENAME)

def get_settings() -> Settings | None:
    with shelve.open(SETTINGS_FILE_LOCATION) as storage:
        if SETTINGS_SHELVE_KEY in storage:
            return storage[SETTINGS_SHELVE_KEY]
        return Settings()


def set_settings(settings: Settings):
    with shelve.open(SETTINGS_FILE_LOCATION) as storage:
        storage[SETTINGS_SHELVE_KEY] = settings


def are_kdm_fetch_settings_valid() -> bool:
    settings = get_settings()

    if not settings or not settings.email_connection_settings:
        return False

    for _, value in vars(settings.email_connection_settings).items():
        if value is None:
            return False
        
    if not settings.scan_n_latest_emails or settings.scan_n_latest_emails <= 0:
        return False

    return True